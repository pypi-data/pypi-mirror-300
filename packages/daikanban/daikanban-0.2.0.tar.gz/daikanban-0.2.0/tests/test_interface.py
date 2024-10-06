from contextlib import suppress
import shutil

from pydantic_core import Url
import pytest

from daikanban.board import Board
from daikanban.config import get_config
from daikanban.errors import BoardNotLoadedError, TaskStatusError
from daikanban.interface import BoardInterface, parse_string_set
from daikanban.model import Project, Task, TaskStatusAction
from daikanban.utils import UserInputError, get_current_time

from . import match_patterns, patch_stdin


def new_board():
    return Board(name='board')


@pytest.mark.parametrize(['s', 'parsed'],[
    ('', None),
    ('a', {'a'}),
    (' a ', {'a'}),
    ('a,b', {'a', 'b'}),
    ('a, b', {'a', 'b'}),
    ('a,\tb', {'a', 'b'}),
    ('" a ",b', {'a', 'b'}),
    ('a b', {'a b'}),
    ('"a, b"', {'a, b'}),
    ("'a, b'", {"'a", "b'"}),
])
def test_parse_string_set(s, parsed):
    assert parse_string_set(s) == parsed


class TestInterface:

    @staticmethod
    def _table_row(cells):
        return r'[│┃]\s*' + r'\s*[│┃]\s*'.join(cells) + r'\s*[│┃]'

    def _test_output(self, capsys, monkeypatch, user_input, out=None, err=None, board=None, interface=None):
        _ = capsys.readouterr()  # clear any extant captured output
        class MockBoardInterface(BoardInterface):
            def save_board(self) -> None:
                # do not attempt to save board to a file
                pass
        if interface is None:
            board = board or new_board()
            interface = MockBoardInterface(board=board)
        if interface.board_path is None:
            interface._set_board_path_to_default()
        for (command, prompt_input) in user_input:
            if prompt_input:
                assert isinstance(prompt_input, list)
                patch_stdin(monkeypatch, ''.join(f'{line}\n' for line in prompt_input))
            try:
                interface.evaluate_prompt(command)
            except EOFError:
                res = capsys.readouterr()
                match_patterns(out, res.out)
                match_patterns(err, res.err)
                raise
        res = capsys.readouterr()
        match_patterns(out, res.out)
        match_patterns(err, res.err)

    # HELP

    @pytest.mark.parametrize(['cmd', 'regex'], [
        ('help', r'User options\s+\[h\]elp\s+show help menu\s+\[q\]uit\s+exit the shell'),
        ('board help', r'Board options\s+\[b\]oard'),
        ('project help', r'Project options\s+\[p\]roject'),
        ('task help', r'Task options\s+\[t\]ask'),
    ])
    def test_help(self, capsys, cmd, regex):
        """Tests output of various shell help commands."""
        self._test_output(capsys, None, [(cmd, None)], regex)

    # PROJECT

    def test_project_show_empty(self, capsys):
        self._test_output(capsys, None, [('project show', None)], r'\[No projects\]')

    def test_project_new(self, capsys, monkeypatch):
        user_input = [('project new', ['proj', 'My project.', '']), ('project show', None), ('project show 0', None)]
        # output of 'project show'
        outputs = [self._table_row(row) for row in [['id', 'name', 'created', '# tasks'], ['0', 'proj', '.*', '0']]]
        # output of 'project show 0'
        outputs.append(r'ID.*0.*name.*proj.*uuid.*description.*My project\.')
        self._test_output(capsys, monkeypatch, user_input, outputs)
        # create project with an invalid name
        user_input = [('project new 123', [])]
        with pytest.raises(UserInputError, match='Project name .* is invalid, must have at least one letter'):
            self._test_output(capsys, monkeypatch, user_input)
        user_input = [('project new', ['123', 'a123', '', ''])]
        self._test_output(capsys, monkeypatch, user_input, out='Project name .* is invalid, must have at least one letter')

    def test_project_new_another(self, capsys, monkeypatch):
        board = new_board()
        board.create_project(Project(name='proj'))
        # add a project with a unique name
        user_input = [('project new', ['proj1'] + [''] * 2)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new project proj1 with ID 1', board=board)
        assert board.get_project(1).name == 'proj1'
        # add a project with the name given rather than prompted
        user_input = [('project new proj2', [''] * 2)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new project proj2 with ID 2', board=board)
        assert board.get_project(2).name == 'proj2'
        # attempt to add project with a duplicate name
        user_input = [('project new proj', [''] * 2)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new project proj with ID 3', err='Duplicate project name', board=board)

    def test_project_set(self, capsys, monkeypatch):
        now = get_current_time()
        board = new_board()
        board.create_project(Project(name='proj'))
        # set an invalid field
        user_input = [('project set 0 fake-field value', None)]
        with pytest.raises(UserInputError, match="Unknown field 'fake-field'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set field on a nonexistent project
        user_input = [('project set 1 name proj1', None)]
        with pytest.raises(UserInputError, match='Project with ID 1 not found'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set the name
        user_input = [('project set 0 name proj0', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        # set the name with '=' expression
        user_input = [('project set 0 name=proj1', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        assert board.get_project(0).name == 'proj1'
        user_input = [('project set 0 name="new project"', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        assert board.get_project(0).name == 'new project'
        # attempt to set an invalid name
        user_input = [('project set 0 name=123', None)]
        with pytest.raises(UserInputError, match='Project name .*123.* is invalid, must have at least one letter'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # NOTE: currently, extra args are permitted but ignored
        user_input = [('project set 0 name=proj0 other stuff', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        proj = board.get_project(0)
        assert proj.name == 'proj0'
        assert proj.description is None
        # set description to empty string (gets converted to None)
        for c in ["'", '"']:
            user_input = [(f'project set 0 description {c}{c}', None)]
            self._test_output(capsys, monkeypatch, user_input, "Updated field 'description'", board=board)
            assert board.get_project(0).description is None
        # set description to null
        user_input = [('project set 0 description', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'description'", board=board)
        assert board.get_project(0).description is None
        # set creation time to valid value
        user_input = [('project set 0 created_time yesterday', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'created_time'", board=board)
        assert board.get_project(0).created_time < now
        # set the set of links
        assert board.get_project(0).links is None
        user_input = [('project set 0 links ""', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'links'", board=board)
        assert board.get_project(0).links is None  # empty set becomes None
        user_input = [('project set 0 links link1', None)]
        with pytest.raises(UserInputError, match='Invalid URL'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        user_input = [('project set 0 links link1.com', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'links'", board=board)
        assert board.get_project(0).links == {Url('https://link1.com')}
        for links in ['link1.com,link2.org', '" link1.com,  link2.org"']:
            user_input = [(f'project set 0 links {links}', None)]
            self._test_output(capsys, monkeypatch, user_input, "Updated field 'links'", board=board)
            assert board.get_project(0).links == {Url('https://link1.com'), Url('https://link2.org')}
        user_input = [('project set 0 links', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'links'", board=board)
        assert board.get_project(0).links is None
        # attempt to set fields to invalid values
        user_input = [('project set 0 name', None)]
        with pytest.raises(UserInputError, match='Input should be a valid string'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        user_input = [('project set 0 created_time', None)]
        with pytest.raises(UserInputError, match='Input should be a valid datetime'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        user_input = [('project set 0 created_time abc', None)]
        with pytest.raises(UserInputError, match="Invalid time 'abc'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set duplicate project name
        board.create_project(Project(name='proj'))
        # set project parent
        user_input = [('project set 1 parent 0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'parent' for project proj with ID 1", board=board)
        user_input = [('project set 1 parent proj0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'parent' for project proj with ID 1", board=board)
        # set project parent to invalid value
        user_input = [('project set 1 parent 2', None)]
        with pytest.raises(UserInputError, match='Project with ID 2 not found'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        user_input = [('project set 1 parent fake', None)]
        with pytest.raises(UserInputError, match='Invalid project name'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # rename project to duplicate another one
        user_input = [('project set 1 name proj0', None)]
        self._test_output(capsys, monkeypatch, user_input, err='Duplicate project name', board=board)
        # attempt to set the project ID
        user_input = [('project set 1 project_id 2', None)]
        with pytest.raises(UserInputError, match="Field 'project_id' cannot be updated"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to set an invalid field
        user_input = [('project set 1 fake abc', None)]
        with pytest.raises(UserInputError, match="Unknown field 'fake'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to set parent to ambiguous project name
        user_input = [('project set 1 parent proj0', None)]
        with pytest.raises(UserInputError, match="Ambiguous project name 'proj0'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)

    # TASK

    def test_task_show_empty(self, capsys):
        self._test_output(capsys, None, [('task show', None)], r'\[No tasks\]')

    def test_task_new(self, capsys, monkeypatch):
        user_input = [('task new', ['task', 'My task.', '', '7', '', '', '', '']), ('task show', None), ('task show 0', None)]
        # output of 'task show'
        outputs = [self._table_row(row) for row in [['id', 'name', 'pri…ty', 'create', 'status'], ['0', 'task', '7', '.*', 'todo']]]
        # output of 'task show 0'
        outputs.append(r'ID.*0.*name.*task.*uuid.*description.*My task\..*created_time.*status.*todo.*project')
        self._test_output(capsys, monkeypatch, user_input, outputs)
        # create task with an invalid name
        user_input = [('task new 123', [])]
        with pytest.raises(UserInputError, match='Task name .* is invalid, must have at least one letter'):
            self._test_output(capsys, monkeypatch, user_input)
        user_input = [('task new', ['123', 'a123', '', '', '', '', '', ''])]
        self._test_output(capsys, monkeypatch, user_input, out='Task name .* is invalid, must have at least one letter')

    def test_task_new_another(self, capsys, monkeypatch):
        board = new_board()
        board.create_task(Task(name='task'))
        # add a task with a unique name
        user_input = [('task new', ['task1'] + [''] * 7)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new task task1 with ID 1', board=board)
        assert board.get_task(1).name == 'task1'
        # add a task with the name given rather than prompted
        user_input = [('task new task2', [''] * 7)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new task task2 with ID 2', board=board)
        assert board.get_task(2).name == 'task2'
        # add task with duplicate name
        user_input = [('task new task', [''] * 7)]
        self._test_output(capsys, monkeypatch, user_input, out='Created new task task with ID 3', err='Duplicate task name', board=board)

    def test_task_begin(self, capsys, monkeypatch):
        now = get_current_time()
        board = new_board()
        board.create_task(Task(name='task0'))
        user_input = [('task begin 0', [''])]
        self._test_output(capsys, monkeypatch, user_input, r'\[0\] to active state', board=board)
        task = board.get_task(0)
        assert task.first_started_time > task.created_time
        # attempt to start a task before its creation time, but decline to
        board.create_task(Task(name='task1'))
        user_input = [('task begin 1', ['yesterday', 'n', 'now'])]
        self._test_output(capsys, monkeypatch, user_input, r'\[1\] to active state', board=board)
        task = board.get_task(1)
        assert task.first_started_time > task.created_time
        # start a task before its creation time, overwrite its creation time
        board.create_task(Task(name='task2'))
        user_input = [('task begin 2', ['yesterday', 'y'])]
        self._test_output(capsys, monkeypatch, user_input, r'\[2\] to active state', board=board)
        task = board.get_task(2)
        assert task.first_started_time == task.created_time
        assert task.first_started_time < now

    def test_task_complete(self, capsys, monkeypatch):
        now = get_current_time()
        board = new_board()
        # complete a task without starting it
        board.create_task(Task(name='task0'))
        user_input = [('task complete 0', ['now', 'now'])]
        self._test_output(capsys, monkeypatch, user_input, r'\[0\] to complete state', board=board)
        task = board.get_task(0)
        assert task.created_time > now
        assert task.first_started_time > task.created_time
        assert task.completed_time > task.first_started_time
        # complete task before start time, but after creation time
        board.create_task(Task(name='task1'))
        user_input = [('task complete 1', ['in 2 days', 'in 1 day'])]
        with pytest.raises(TaskStatusError, match='cannot complete a task before its last started time'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to create a task before creation time, but decline to
        board.create_task(Task(name='task2'))
        user_input = [('task complete 2', ['yesterday', 'n'])]
        with suppress(EOFError):
            self._test_output(capsys, monkeypatch, user_input, 'Cannot start a task before its creation time', board=board)
        # complete task before creation time, but after start time
        board.create_task(Task(name='task3'))
        user_input = [('task complete 3', ['2 days ago', 'y', 'yesterday'])]
        outputs = ['Set creation time', r'\[3\] to complete state']
        self._test_output(capsys, monkeypatch, user_input, outputs, board=board)
        task = board.get_task(3)
        assert task.created_time < now
        assert task.first_started_time == task.created_time
        assert task.completed_time > task.first_started_time
        # complete task before creation time and before start time
        board.create_task(Task(name='task3'))
        user_input = [('task complete 4', ['yesterday', 'y', '2 days ago', 'y'])]
        with pytest.raises(TaskStatusError, match='cannot complete a task before its last started time'):
            self._test_output(capsys, monkeypatch, user_input, board=board)

    def test_task_set(self, capsys, monkeypatch):
        now = get_current_time()
        board = new_board()
        board.create_task(Task(name='task', description='task'))
        # set the name
        user_input = [('task set 0 name task0', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        # set the name with '=' expression
        user_input = [('task set 0 name=task1', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        assert board.get_task(0).name == 'task1'
        user_input = [('task set 0 name="new task"', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        assert board.get_task(0).name == 'new task'
        # NOTE: currently, extra args are permitted but ignored
        user_input = [('task set 0 name=task0 other stuff', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'name'", board=board)
        task = board.get_task(0)
        assert task.name == 'task0'
        assert task.description == 'task'
        # attempt to set an invalid name
        user_input = [('task set 0 name=123', None)]
        with pytest.raises(UserInputError, match='Task name .*123.* is invalid, must have at least one letter'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set description to null
        user_input = [('task set 0 description', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'description'", board=board)
        assert board.get_task(0).description is None
        # attempt to set start time earlier than created time
        user_input = [('task set 0 first_started_time yesterday', None)]
        with pytest.raises(UserInputError, match='Task start time cannot precede created time'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to set created time later than start time
        user_input = [('task set 0 first_started_time tomorrow', None)]
        self._test_output(capsys, monkeypatch, user_input, "Updated field 'first_started_time'", board=board)
        assert board.get_task(0).first_started_time > now
        user_input = [('task set 0 created_time "in two days"', None)]
        with pytest.raises(UserInputError, match='Task start time cannot precede created time'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to set a computed field
        user_input = [('task set 0 status todo', None)]
        with pytest.raises(UserInputError, match="Field 'status' cannot be updated"):
            self._test_output(capsys, monkeypatch, user_input, "Updated field 'description'", board=board)
        # attempt to set fields to invalid values
        user_input = [('task set 0 name', None)]
        with pytest.raises(UserInputError, match='Input should be a valid string'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # attempt to set duplicate task name
        board.create_task(Task(name='task'))
        user_input = [('task set 1 name task0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'name'", err='Duplicate task name', board=board)
        # attempt to set the task ID
        user_input = [('task set 1 task_id 2', None)]
        with pytest.raises(UserInputError, match="Field 'task_id' cannot be updated"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set the project ID to an invalid project
        user_input = [('task set 1 project_id 0', None)]
        with pytest.raises(UserInputError, match='Project with ID 0 not found'):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set the project ID to a valid project
        assert board.create_project(Project(name='proj')) == 0
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'project_id' for task task0 with ID 1", board=board)
        # update the project ID via "project" instead of "project_id"
        user_input = [('task set 1 project 0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'project_id' for task task0 with ID 1", board=board)
        # update the project ID via its name
        user_input = [('task set 1 project proj', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'project_id' for task task0 with ID 1", board=board)
        # attempt to use a project name instead of ID with "project_id"
        user_input = [('task set 1 project_id proj', None)]
        with pytest.raises(UserInputError, match="Invalid project ID 'proj'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # unset the project ID
        for cmd in ['task set 1 project', 'task set 1 project_id', 'task set 1 project=', "task set 1 project=''", "task set 1 project_id=''"]:
            user_input = [(cmd, None)]
            self._test_output(capsys, monkeypatch, user_input, out="Updated field 'project_id' for task task0 with ID 1", board=board)
        # set task parent
        user_input = [('task set 1 parent 0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'parent' for task task0 with ID 1", board=board)
        # set task parent to ambiguous task name
        user_input = [('task set 1 parent task0', None)]
        with pytest.raises(UserInputError, match="Ambiguous task name 'task0'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # name 'task' matches two instances of 'task0' (fuzzily)
        user_input = [('task set 1 parent task', None)]
        with pytest.raises(UserInputError, match="Ambiguous task name 'task'"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        # set blocking tasks
        user_input = [('task set 1 blocked_by 0', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'blocked_by' for task task0 with ID 1", board=board)
        assert board.get_task(1).blocked_by == {0}
        user_input = [('task set 1 blocked_by 0,1', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'blocked_by' for task task0 with ID 1", board=board)
        assert board.get_task(1).blocked_by == {0, 1}
        user_input = [('task set 1 blocked_by 2', None)]
        with pytest.raises(UserInputError, match="Task with ID 2 not found"):
            self._test_output(capsys, monkeypatch, user_input, board=board)
        board.update_task(1, name='task1')
        user_input = [('task set 1 blocked_by 0,task1', None)]
        self._test_output(capsys, monkeypatch, user_input, out="Updated field 'blocked_by' for task task1 with ID 1", board=board)
        assert board.get_task(1).blocked_by == {0, 1}

    # BOARD

    def test_board_new(self, capsys, monkeypatch, set_tmp_board_path, use_regular_print):
        """Tests 'board new'."""
        board_cfg = get_config().board
        board_dir = board_cfg.board_dir_path
        default_out = ['Creating new DaiKanban board.']
        out = default_out + ['Board name:', 'Output filename', r'\(.*board_1.json\)', 'Board description', r'Saved DaiKanban board .*Board 1.*to .*board\_1\.json']
        self._test_output(capsys, monkeypatch, [('board new', ['Board 1', '', ''])], out=out, interface=BoardInterface())
        # name gets converted to snake case
        assert (board_dir / 'board_1.json').exists()
        out = default_out + ['Output filename', r'\(.*board2.json\)', 'Board description', r'Saved DaiKanban board .*board2.*to .*board2\.json']
        self._test_output(capsys, monkeypatch, [('board new board2', ['', ''])], out=out, interface=BoardInterface())
        assert (board_dir / 'board2.json').exists()
        out = default_out + ['Output filename', r'\(.*board3.json\)', 'Board description', r'Saved DaiKanban board .*board3.*to .*myboard\.json']
        self._test_output(capsys, monkeypatch, [('board new board3', ['myboard.json', ''])], out=out, interface=BoardInterface())
        assert (board_dir / 'myboard.json').exists()
        assert not (board_dir / 'board3.json').exists()
        out = default_out + [r'Board name \(board3\):', 'Board description', r'Saved DaiKanban board .*myboard.*to .*board3\.json']
        self._test_output(capsys, monkeypatch, [('board new board3.json', ['myboard', ''])], out=out, interface=BoardInterface())
        assert (board_dir / 'board3.json').exists()
        out = default_out + [r'Board name \(board4\):', 'Board description', r'Saved DaiKanban board .*board4.*to .*board4\.json']
        self._test_output(capsys, monkeypatch, [('board new board4.json', ['', ''])], out=out, interface=BoardInterface())
        assert (board_dir / 'board4.json').exists()
        # delete board directory: creating a new board should create it again
        shutil.rmtree(board_dir)
        out = default_out + ['Board name:', 'Output filename', r'\(.*board1.json\)', 'Board description', r'Saved DaiKanban board .*board1.*to .*board1\.json']
        self._test_output(capsys, monkeypatch, [('board new', ['board1', '', ''])], out=out, interface=BoardInterface())
        assert (board_dir / 'board1.json').exists()

    def test_board_show_empty(self, capsys):
        """Tests 'board show' when there are no tasks."""
        self._test_output(capsys, None, [('board show', None)], out=r'\[No tasks\]')

    def test_board_show_one_task(self, capsys, monkeypatch):
        """Tests 'board show' through the life cycle of a single task."""
        board = new_board()
        user_input = [('task new', ['task', 'My task.', '', '7', '', '', '', '']), ('board show', None)]
        outputs = [r'todo \(1\)'] + [self._table_row(row) for row in [['id', 'name', 'score'], ['0', 'task', '.*']]]
        self._test_output(capsys, monkeypatch, user_input, outputs, board=board)
        user_input = [('task begin 0', ['']), ('board show', None)]
        outputs = [r'active \(1\)', 'Score:']
        self._test_output(capsys, monkeypatch, user_input, outputs, board=board)
        user_input = [('task complete 0', ['']), ('board show', None)]
        outputs = [r'complete \(1\)', 'last', self._table_row(['id', 'name', 'completed'])]
        self._test_output(capsys, monkeypatch, user_input, outputs, board=board)

    def test_board_sort_tasks(self, capsys, monkeypatch):
        """Tests how tasks are sorted in 'board show'."""
        board = new_board()
        for i in range(3):
            board.create_task(Task(name=f'task{i}'))
            board.apply_status_action(i, TaskStatusAction.start)
        board.apply_status_action(1, TaskStatusAction.pause)
        interface = BoardInterface(board=board)
        cfg = get_config()
        task_rows_by_col = interface._get_task_rows_by_column()
        assert list(task_rows_by_col) == ['active']
        names = [row.name for row in task_rows_by_col['active']]
        # active tasks are shown before paused
        assert names == ['task0', 'task2', 'task1 ⏸️ ']
        # sort tasks by name instead
        cfg.display.columns['active'].sort_by = 'name'
        interface = BoardInterface(board=board, config=cfg)
        task_rows_by_col = interface._get_task_rows_by_column()
        names = [row.name for row in task_rows_by_col['active']]
        # status column should *not* be shown
        with pytest.raises(AssertionError, match="pattern 'status' not found"):
            self._test_output(capsys, monkeypatch, [('board show', None)], ['status'], board=board)

    def test_board_load_and_list(self, capsys, monkeypatch, populate_board_dir, use_regular_print):
        """Tests the behavior of 'board load' and 'board list'."""
        board_cfg = get_config().board
        board_dir = board_cfg.board_dir_path
        no_default_msg = 'No default board exists. You can create one with:'
        no_board_msg = 'Board file does not exist. You can create it with:'
        # default board gets loaded
        interface = BoardInterface()
        out = r'  \* board.json\n    empty_board.json\n    empty_file.JSON\n'
        self._test_output(capsys, monkeypatch, [('board list', None)], out=out, err=f'Board directory: {board_dir}', interface=interface)
        out = ['Loading default board', 'To switch boards', 'Loaded board with 1 project, 3 tasks']
        self._test_output(capsys, monkeypatch, [('board load', None), ('board show', None)], out=out, interface=interface)
        # load nonexistent board
        self._test_output(capsys, monkeypatch, [('board load fake_board.json', None)], out=no_board_msg, interface=interface)
        # delete default board
        board_cfg.default_board_path.unlink()
        interface = BoardInterface()
        out = [no_default_msg, '  empty_board.json\n  empty_file.JSON\n']
        self._test_output(capsys, monkeypatch, [('board list', None)], out=out, err=f'Board directory: {board_dir}', interface=interface)
        out = [no_default_msg, 'Default board file does not exist. You can create it with:']
        self._test_output(capsys, monkeypatch, [('board load', None)], out=out, interface=interface)
        with pytest.raises(BoardNotLoadedError, match='No board has been loaded.'):
            self._test_output(capsys, monkeypatch, [('board show', None)], interface=interface)
        # delete all boards
        for p in board_dir.glob('*'):
            p.unlink()
        interface = BoardInterface()
        self._test_output(capsys, monkeypatch, [('board list', None)], out=no_default_msg, err=f'Board directory: {board_dir}', interface=interface)
        with pytest.raises(BoardNotLoadedError, match='No board has been loaded.'):
            self._test_output(capsys, monkeypatch, [('board show', None)], interface=interface)
