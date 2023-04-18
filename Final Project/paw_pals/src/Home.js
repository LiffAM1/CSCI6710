import React, { useEffect, useState } from 'react';
import { useCookies } from 'react-cookie';

function Home() {
  const [cookies, setCookie] = useCookies(['session_id']);
  const [session, setSession] = useState(false);

  useEffect(() => {
    var session_id = cookies.session_id;
    console.log(session_id);
    if (session_id) {
      fetch('https://localhost:5000/session/' + session_id,
        {
          credentials: 'include',
          method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
          setSession(data);
        });
    }
  });

  if (session)
    return <div>Logged in!</div>
  return <a href="https://localhost:5000/login">Login</a>
}


export default Home;
