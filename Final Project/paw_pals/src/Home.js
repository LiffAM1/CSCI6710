import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios'

function Home() {
  const state = { authenticated:false}

  if (state.authenticated)
    return <div>Home</div>
  return <a href="https://localhost:5000/login">Login</a>
}

export default Home;
