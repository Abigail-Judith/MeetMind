function Dashboard() {
    const username = "Abigail";

    return (
        <div className="dashboard">

            <header className="dashboard-header">
                <div>
                    <h1>MeetMind</h1>
                    <p>AI-powered meeting intelligence</p>
                </div>

                <button>
                    Logout
                </button>
            </header>

            <main className="dashboard-content">

                <section className="welcome-section">
                    <h2>Welcome back, {username} 👋</h2>
                    <p>
                        Manage your meetings, transcripts, summaries and tasks
                        from one place.
                    </p>
                </section>

                <section className="dashboard-grid">

                    <div className="dashboard-card">
                        <h3>📅 Meetings</h3>
                        <p>
                            Create and manage your meetings.
                        </p>
                        <button>
                            View Meetings
                        </button>
                    </div>

                    <div className="dashboard-card">
                        <h3>🎙️ Audio Transcription</h3>
                        <p>
                            Upload meeting audio and generate transcripts.
                        </p>
                        <button>
                            Upload Audio
                        </button>
                    </div>

                    <div className="dashboard-card">
                        <h3>📄 Documents</h3>
                        <p>
                            Upload PDF or Word documents for AI-powered search.
                        </p>
                        <button>
                            Upload Document
                        </button>
                    </div>

                    <div className="dashboard-card">
                        <h3>🤖 Ask MeetMind</h3>
                        <p>
                            Ask questions about your meeting information.
                        </p>
                        <button>
                            Ask AI
                        </button>
                    </div>

                    <div className="dashboard-card">
                        <h3>📝 Summaries</h3>
                        <p>
                            Generate AI-powered meeting summaries.
                        </p>
                        <button>
                            View Summaries
                        </button>
                    </div>

                    <div className="dashboard-card">
                        <h3>✅ Action Items</h3>
                        <p>
                            Track tasks and deadlines extracted from meetings.
                        </p>
                        <button>
                            View Tasks
                        </button>
                    </div>

                </section>

            </main>

        </div>
    );
}

export default Dashboard;