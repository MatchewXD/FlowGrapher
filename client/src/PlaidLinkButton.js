import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlaidLinkButton = () => {
  const [linkToken, setLinkToken] = useState('');

  useEffect(() => {
    // Fetch the link token from the Flask backend
    const fetchLinkToken = async () => {
      const response = await axios.get('/create_link_token');
      setLinkToken(response.data.link_token);
    };

    fetchLinkToken();
  }, []);

  const handlePlaidLink = () => {
    const handler = window.Plaid.create({
      token: linkToken,
      onSuccess: (public_token, metadata) => {
        // Send the public token to your Flask backend to exchange it for an access token
        axios.post('/exchange_public_token', { public_token })
          .then(response => {
            console.log('Access token:', response.data.access_token);
          })
          .catch(error => {
            console.error('Error exchanging public token:', error);
          });
      },
      onExit: (err, metadata) => {
        if (err != null) {
          console.error('Plaid Link error:', err);
        }
      }
    });

    handler.open();
  };

  return (
    <button onClick={handlePlaidLink} disabled={!linkToken}>
      Connect a bank account
    </button>
  );
};

export default PlaidLinkButton;
