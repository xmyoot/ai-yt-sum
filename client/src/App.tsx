import React, { useState } from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import ProTip from "./ProTip";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";

function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{" "}
      {new Date().getFullYear()}.
    </Typography>
  );
}

export default function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [summaries, setSummaries] = useState([]);
  const [error, setError] = useState("");
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!url.startsWith("https://www.youtube.com/")) {
      setError("URL must start with https://www.youtube.com/");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });
      const data = await response.json();
      setSummaries(data); // update the summaries state with the response data
      setLoading(false);
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };
  const renderList = (summaries: any) => {
    return (
      <Container maxWidth="lg">
        <Typography variant="h4" component="h2" sx={{ m: 2 }}>
          Video Summary:
        </Typography>
        <List
          sx={{
            bgcolor: "background.paper",
            border: "1px solid lightgrey",
            borderRadius: "5px",
          }}
        >
          {summaries["Summarized Video:"] &&
            Array.isArray(summaries["Summarized Video:"]) &&
            summaries["Summarized Video:"].map((summary, index) => (
              <ListItem key={index}>
                <ListItemButton>
                  <Typography variant="h6" sx={{ m: 2 }}>
                    {Object.keys(summary)[0]}:
                  </Typography>
                  {summary[Object.keys(summary)[0]]}
                </ListItemButton>
              </ListItem>
            ))}
        </List>
      </Container>
    );
  };
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" sx={{ m: 2 }}>
          AI Youtube Summarizer
        </Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField
            label="Enter a YouTube URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            fullWidth
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            sx={{ m: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : "Summarize Now"}
          </Button>
        </form>
        {loading ? (
          <CircularProgress size={24} />
        ) : (
          summaries && renderList(summaries)
        )}
        <ProTip />
        <Copyright />
      </Box>
    </Container>
  );
}
