import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Meetings() {
    const navigate = useNavigate();

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [meetingTime, setMeetingTime] = useState("");

    const [meetings, setMeetings] = useState([]);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    // Load existing meetings when page opens
    const fetchMeetings = async () => {
        try {
            const token = localStorage.getItem("token");

            const response = await api.get(
                "/meetings",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setMeetings(response.data);

        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Could not load meetings."
            );
        }
    };

    // Run fetchMeetings when the page loads
    useEffect(() => {
        fetchMeetings();
    }, []);

    // Create a new meeting
    const handleCreateMeeting = async (e) => {
        e.preventDefault();

        setError("");
        setSuccess("");
        setLoading(true);

        try {
            const token = localStorage.getItem("token");

            const response = await api.post(
                "/meetings",
                {
                    title: title,
                    description: description,
                    meeting_time: meetingTime
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            // Add the new meeting to the list
            setMeetings((previousMeetings) => [
                ...previousMeetings,
                response.data
            ]);

            // Clear the form
            setTitle("");
            setDescription("");
            setMeetingTime("");

            setSuccess("Meeting created successfully!");

        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Could not create meeting."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard">

            {/* Header */}
            <header className="dashboard-header">

                <div>
                    <h1>MeetMind</h1>
                    <p>Meetings</p>
                </div>

                <button
                    onClick={() => navigate("/dashboard")}
                >
                    ← Dashboard
                </button>

            </header>


            {/* Main Content */}
            <main className="dashboard-content">

                <section className="welcome-section">

                    <h2>
                        Meetings 📅
                    </h2>

                    <p>
                        Create and manage your meetings.
                    </p>

                </section>


                {/* Create Meeting */}
                <section className="dashboard-card">

                    <h3>
                        Create New Meeting
                    </h3>

                    <form onSubmit={handleCreateMeeting}>

                        <input
                            type="text"
                            placeholder="Meeting title"
                            value={title}
                            onChange={(e) =>
                                setTitle(e.target.value)
                            }
                            required
                        />

                        <br />
                        <br />

                        <textarea
                            placeholder="Meeting description"
                            value={description}
                            onChange={(e) =>
                                setDescription(e.target.value)
                            }
                            rows="4"
                        />

                        <br />
                        <br />

                        <input
                            type="datetime-local"
                            value={meetingTime}
                            onChange={(e) =>
                                setMeetingTime(e.target.value)
                            }
                            required
                        />

                        <br />
                        <br />

                        <button
                            type="submit"
                            disabled={loading}
                        >
                            {loading
                                ? "Creating..."
                                : "Create Meeting"}
                        </button>

                    </form>

                    {success && (
                        <p className="success-message">
                            {success}
                        </p>
                    )}

                    {error && (
                        <p className="error-message">
                            {error}
                        </p>
                    )}

                </section>


                {/* Meetings List */}
                <section className="meeting-list">

                    <h3>
                        Your Meetings
                    </h3>

                    {meetings.length === 0 ? (

                        <p>
                            No meetings created yet.
                        </p>

                    ) : (

                        <div className="dashboard-grid">

                            {meetings.map((meeting) => (

                                <div
                                    className="dashboard-card"
                                    key={meeting.id}
                                >

                                    <h3>
                                        📅 {meeting.title}
                                    </h3>

                                    <p>
                                        {meeting.description ||
                                            "No description provided."}
                                    </p>

                                    <p>
                                        <strong>
                                            Date:
                                        </strong>{" "}
                                        {meeting.meeting_time}
                                    </p>

                                </div>

                            ))}

                        </div>

                    )}

                </section>

            </main>

        </div>
    );
}

export default Meetings;