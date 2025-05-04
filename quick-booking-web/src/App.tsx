import React, { useEffect, useMemo, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HotelListing from './pages/HotelListing';
import { getUserInfo } from './utils/cookie';

function App() {

  const [isLoading, setIsLoading] = useState(true);

  const user = useMemo(() => {
    try {
      return getUserInfo();
    }
    catch (e) {
      console.error(e);
      return null;
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleLogout = () => {
    // Clear user info from cookies/storage
    document.cookie = 'userInfo=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    const sessionHint = document.cookie.split('; ')
      .find(row => row.startsWith('session_hint='))
      ?.split('=')[1] || '';
    window.location.href = `/auth/logout?session_hint=${sessionHint}`;
  };

  if (!user && !isLoading) {
    window.location.href = '/auth/login';
  }

  return (
      <Router>
        <nav style={{ backgroundColor: '#335', padding: '0.25rem', boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxWidth: '1200px', margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <h1 style={{ color: '#fff', fontSize: '1.5rem', fontWeight: 600 }}>
                Welcome, {user?.username || 'Guest'}
              </h1>
            </div>
            <button 
              style={{
                padding: '0.75rem 1.5rem',
                color: '#fff',
                backgroundColor: '#555',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 500,
                boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.1)',
                transition: 'background-color 0.2s ease-in-out'
              }}
              onClick={handleLogout}
            >
              Sign Out
            </button>
          </div>
        </nav>
        <Routes>
          {user && (
            <Route path="/" element={<HotelListing />} />
          )}
        </Routes>
      </Router>
  );
}

export default App;
