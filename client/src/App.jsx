import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';


function App() {
  const [events, setEvents] = useState()

  useEffect(() => {
    const fetchEvents = async () => {
      const response = await axios.get('http://127.0.0.1:5000/events')
      console.log(response.data, "data")
      setEvents(response.data);
    };
    const interval = setInterval(fetchEvents, 15000);
    fetchEvents(); // Fetch initially
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <div className="App">
        <h1>Recent Events</h1>
        <ul>
          {events?.map((event, index) => (
            <li key={index}>
              {renderEvent(event)}
            </li>
          ))}
        </ul>
      </div>
    </>
  )
}

function renderEvent(event) {
  const timestamp = new Date(event.timestamp).toUTCString();
  if (event.action_type === 'push') {
    return `${event.author} pushed to ${event.to_branch} on ${timestamp}`;
  } else if (event.action_type === 'pull_request') {
    return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
  } else if (event.action_type === 'merge') {
    return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
  }
}

export default App
