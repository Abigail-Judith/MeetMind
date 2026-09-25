import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

function MeetingWorkspace() {
    const navigate = useNavigate();
    const { meetingId } = useParams();

    const fileInputRef = useRef(null);

    const [meeting, setMeeting] = useState(null);
    const [meetingError, setMeetingError] = useState("");

    const [transcript, setTranscript] = useState("");
    const [uploading, setUploading] = useState(false);
    const [audioError, setAudioError] = useState("");

    // Load meeting details
    const fetchMeeting = async () => {
        try {
            const token = localStorage.getItem("token");

            const response = await api.get(
                `/meetings/${meetingId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setMeeting(response.data);

        } catch (error) {
            setMeetingError(
                error.response?.data?.detail ||
                "Could not load meeting."
            );
        }
    };

    // Load meeting when page opens
    useEffect(() => {
        fetchMeeting();
    }, [meetingId]);


    // Upload and transcribe audio
    const handleAudioUpload = async (event) => {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setAudioError("");
        setTranscript("");
        setUploading(true);

        try {
            const token = localStorage.getItem("token");

            const formData = new FormData();
            formData.append("file", file);

            const response = await api.post(
                `/audio/upload/${meetingId}`,
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setTranscript(response.data.transcript);

        } catch (error) {
            setAudioError(
                error.response?.data?.detail ||
                "Could not upload and transcribe the audio."
            );
        } finally {
            setUploading(false);

            // Allow the same file to be selected again
            event.target.value = "";
        }
    };


    const openAudioPicker = () => {
        fileInputRef.current.click();
    };


    return (
        <div className="dashboard">

            {/* Header */}
            <header className="dashboard-header">

                <div>
                    <h1>MeetMind</h1>
                    <p>Meeting Workspace</p>
                </div>

                <button
                    onClick={() => navigate("/meetings")}
                >
                    ← Meetings
                </button>

            </header>


            {/* Main Content */}
            <main className="dashboard-content">

                <section className="welcome-section">

                    <h2>
                        {meeting
                            ? `${meeting.title} 🗓️`
                            : "Loading meeting..."}
                    </h2>

                    <p>
                        {meeting
                            ? "Your AI-powered meeting workspace."
                            : "Please wait while we load your meeting."}
                    </p>

                    {meetingError && (
                        <p className="error-message">
                            {meetingError}
                        </p>
                    )}

                </section>


                {/* Workspace Features */}
                <section className="dashboard-grid">

                    {/* Audio */}
                    <div className="dashboard-card">

                        <h3>
                            🎙️ Audio Transcription
                        </h3>

                        <p>
                            Upload meeting audio and generate
                            a transcript using Whisper AI.
                        </p>

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="audio/*"
                            onChange={handleAudioUpload}
                            style={{ display: "none" }}
                        />

                        <button
                            onClick={openAudioPicker}
                            disabled={uploading}
                        >
                            {uploading
                                ? "Transcribing..."
                                : "Upload Audio"}
                        </button>

                        {audioError && (
                            <p className="error-message">
                                {audioError}
                            </p>
                        )}

                    </div>


                    {/* Documents */}
                    <div className="dashboard-card">

                        <h3>📄 Documents</h3>

                        <p>
                            Upload PDF or Word documents
                            for semantic search.
                        </p>

                        <button>
                            Upload Document
                        </button>

                    </div>


                    {/* AI */}
                    <div className="dashboard-card">

                        <h3>🤖 Ask MeetMind</h3>

                        <p>
                            Ask questions about this meeting
                            using AI and RAG.
                        </p>

                        <button>
                            Ask AI
                        </button>

                    </div>


                    {/* Summary */}
                    <div className="dashboard-card">

                        <h3>📝 Meeting Summary</h3>

                        <p>
                            Generate an AI-powered summary
                            of this meeting.
                        </p>

                        <button>
                            Generate Summary
                        </button>

                    </div>


                    {/* Tasks */}
                    <div className="dashboard-card">

                        <h3>✅ Action Items</h3>

                        <p>
                            Extract and manage tasks,
                            people and deadlines.
                        </p>

                        <button>
                            View Action Items
                        </button>

                    </div>


                    {/* Conversation History */}
                    <div className="dashboard-card">

                        <h3>💬 Conversation History</h3>

                        <p>
                            View your previous conversations
                            with MeetMind about this meeting.
                        </p>

                        <button>
                            View History
                        </button>

                    </div>

                </section>


                {/* Transcript */}
                {transcript && (
                    <section
                        className="dashboard-card"
                        style={{ marginTop: "30px" }}
                    >

                        <h3>
                            📄 Meeting Transcript
                        </h3>

                        <p
                            style={{
                                whiteSpace: "pre-wrap",
                                lineHeight: "1.7"
                            }}
                        >
                            {transcript}
                        </p>

                    </section>
                )}

            </main>

        </div>
    );
}

export default MeetingWorkspace;