import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import "./App.css";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Meetings from "./pages/Meetings";
import MeetingWorkspace from "./pages/MeetingWorkspace";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* Login */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        {/* Meetings */}
        <Route
          path="/meetings"
          element={<Meetings />}
        />

        {/* Individual Meeting Workspace */}
        <Route
          path="/meetings/:meetingId"
          element={<MeetingWorkspace />}
        />

        {/* Default route */}
        <Route
          path="/"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;