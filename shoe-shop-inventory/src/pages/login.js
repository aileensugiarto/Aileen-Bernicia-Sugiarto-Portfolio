import React, { useState } from "react";
import { Button, TextField, Container, Typography, Box } from '@mui/material';
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    axios.post("http://localhost:5000/api/auth/login", {
      username: username,
      password: password,
    })
      .then(response => {
        // Check if the response indicates a successful login
        if (response.data.success) {
          localStorage.setItem("isAuthenticated", "true"); // Store authentication status
          onLogin(); // Call the onLogin prop to update authentication status in App.js
          navigate("/dashboard"); // Navigate to the dashboard
        } else {
          setError(response.data.message || "Login failed."); // Show error message if login fails
        }
      })
      .catch(error => {
        console.error("Login error:", error); // Log error for debugging
        setError("An error occurred. Please try again."); // Set a generic error message
      });
  };

  return (
    <Container maxWidth="sm">
      <Box mt={10}>
        <Typography variant="h4" gutterBottom>
          Login
        </Typography>
        {error && <Typography color="error">{error}</Typography>}
        <form noValidate autoComplete="off">
          <TextField
            fullWidth
            margin="normal"
            label="Username"
            variant="outlined"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Password"
            type="password"
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
          />
          <Box mt={2}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              onClick={handleLogin}>
              Login
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
};

export default Login;
