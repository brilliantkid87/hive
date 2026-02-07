"""Tests for the TUI module - StatusBar and AdenTUI components."""

import time
from unittest.mock import MagicMock


class TestStatusBarState:
    """Test StatusBar state management (without Textual app context)."""

    def test_format_elapsed_seconds_only(self):
        """Test elapsed time formatting for seconds only."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        assert status_bar._format_elapsed(45) == "0:45"

    def test_format_elapsed_minutes_and_seconds(self):
        """Test elapsed time formatting for minutes and seconds."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        assert status_bar._format_elapsed(125) == "2:05"

    def test_format_elapsed_hours(self):
        """Test elapsed time formatting for hours."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        assert status_bar._format_elapsed(3665) == "1:01:05"

    def test_initial_state_is_idle(self):
        """StatusBar should start in idle state."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        assert status_bar._state == "idle"
        assert status_bar._active_node is None
        assert status_bar._start_time is None

    def test_initial_state_with_graph_id(self):
        """StatusBar should store graph_id from init."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar(graph_id="test_graph")
        assert status_bar._graph_id == "test_graph"

    def test_set_running_updates_state(self):
        """set_running should update state and start timer."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()  # Mock to avoid Textual queries

        status_bar.set_running(entry_node="node_1")

        assert status_bar._state == "running"
        assert status_bar._active_node == "node_1"
        assert status_bar._start_time is not None
        assert status_bar._final_elapsed is None

    def test_set_running_without_entry_node(self):
        """set_running without entry_node should set active_node to None."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        status_bar.set_running()

        assert status_bar._state == "running"
        assert status_bar._active_node is None

    def test_set_completed_updates_state(self):
        """set_completed should update state and record elapsed time."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        # Simulate running first
        status_bar._start_time = time.time() - 10  # Started 10 seconds ago
        status_bar._state = "running"

        status_bar.set_completed()

        assert status_bar._state == "completed"
        assert status_bar._active_node is None
        assert status_bar._start_time is None
        assert status_bar._final_elapsed is not None
        assert status_bar._final_elapsed >= 10

    def test_set_failed_updates_state(self):
        """set_failed should update state and record error."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        status_bar._start_time = time.time() - 5
        status_bar._state = "running"

        status_bar.set_failed(error="Connection timeout")

        assert status_bar._state == "failed"
        assert status_bar._node_detail == "Connection timeout"
        assert status_bar._final_elapsed is not None

    def test_set_failed_truncates_long_errors(self):
        """set_failed should truncate long error messages."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        long_error = "A" * 100
        status_bar.set_failed(error=long_error)

        assert len(status_bar._node_detail) == 40

    def test_set_active_node(self):
        """set_active_node should update active node and detail."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        status_bar.set_active_node("worker_node", detail="processing")

        assert status_bar._active_node == "worker_node"
        assert status_bar._node_detail == "processing"

    def test_set_node_detail(self):
        """set_node_detail should update only the detail."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()
        status_bar._active_node = "some_node"

        status_bar.set_node_detail("step 5")

        assert status_bar._active_node == "some_node"
        assert status_bar._node_detail == "step 5"

    def test_set_graph_id(self):
        """set_graph_id should update the graph ID."""
        from framework.tui.app import StatusBar

        status_bar = StatusBar()
        status_bar._refresh = MagicMock()

        status_bar.set_graph_id("new_graph_id")

        assert status_bar._graph_id == "new_graph_id"


class TestStatusBarCSS:
    """Test StatusBar CSS configuration."""

    def test_default_css_exists(self):
        """StatusBar should have DEFAULT_CSS defined."""
        from framework.tui.app import StatusBar

        assert hasattr(StatusBar, "DEFAULT_CSS")
        assert "StatusBar" in StatusBar.DEFAULT_CSS
        assert "dock: top" in StatusBar.DEFAULT_CSS


class TestAdenTUIConfiguration:
    """Test AdenTUI class configuration (without running the app)."""

    def test_title_constant(self):
        """AdenTUI should have correct title."""
        from framework.tui.app import AdenTUI

        assert AdenTUI.TITLE == "Aden TUI Dashboard"

    def test_bindings_defined(self):
        """AdenTUI should have key bindings defined."""
        from framework.tui.app import AdenTUI

        assert hasattr(AdenTUI, "BINDINGS")
        assert len(AdenTUI.BINDINGS) > 0

        # Check for essential bindings
        binding_keys = [b.key for b in AdenTUI.BINDINGS]
        assert "q" in binding_keys  # Quit
        assert "ctrl+c" in binding_keys  # Interrupt
        assert "ctrl+s" in binding_keys  # Screenshot
        assert "tab" in binding_keys  # Focus next

    def test_css_defined(self):
        """AdenTUI should have CSS defined."""
        from framework.tui.app import AdenTUI

        assert hasattr(AdenTUI, "CSS")
        assert "Screen" in AdenTUI.CSS
        assert "GraphOverview" in AdenTUI.CSS
        assert "ChatRepl" in AdenTUI.CSS

    def test_event_types_defined(self):
        """AdenTUI should have event types list."""
        from framework.tui.app import AdenTUI

        assert hasattr(AdenTUI, "_EVENT_TYPES")
        assert len(AdenTUI._EVENT_TYPES) > 0

    def test_log_pane_events_subset(self):
        """Log pane events should be a subset of all events."""
        from framework.tui.app import AdenTUI

        assert hasattr(AdenTUI, "_LOG_PANE_EVENTS")
        # Log pane events should exclude delta events
        assert len(AdenTUI._LOG_PANE_EVENTS) <= len(AdenTUI._EVENT_TYPES)


class TestAdenTUIInitialization:
    """Test AdenTUI initialization with mocked runtime."""

    def test_init_stores_runtime(self):
        """AdenTUI should store the runtime reference."""
        from framework.tui.app import AdenTUI

        # Create mock runtime
        mock_runtime = MagicMock()
        mock_runtime.graph.id = "test_graph"

        app = AdenTUI(runtime=mock_runtime)

        assert app.runtime == mock_runtime
        assert app.is_ready is False

    def test_init_creates_widgets(self):
        """AdenTUI should create widget instances."""
        from framework.tui.app import AdenTUI

        mock_runtime = MagicMock()
        mock_runtime.graph.id = "test_graph"

        app = AdenTUI(runtime=mock_runtime)

        assert app.log_pane is not None
        assert app.graph_view is not None
        assert app.chat_repl is not None
        assert app.status_bar is not None

    def test_status_bar_has_graph_id(self):
        """StatusBar should be initialized with graph ID."""
        from framework.tui.app import AdenTUI

        mock_runtime = MagicMock()
        mock_runtime.graph.id = "my_agent_graph"

        app = AdenTUI(runtime=mock_runtime)

        assert app.status_bar._graph_id == "my_agent_graph"
