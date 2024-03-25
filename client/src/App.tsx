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
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import logo from "./assets/logo.svg";

function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        AI Youtube Summarizer, LLC
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
  const handlePrintPDF = () => {
    const markdown = generateMarkdown(summaries);
    printPDF(markdown);
  };

  const generateMarkdown = (summaries: any) => {
    let markdown = "";
    if (
      summaries["Summarized Video:"] &&
      Array.isArray(summaries["Summarized Video:"])
    ) {
      summaries["Summarized Video:"].forEach((summary: any, index: number) => {
        const title = Object.keys(summary)[0];
        const content = summary[title].summary;
        markdown += `## ${title}\n\n${content}\n\n`;
      });
    }
    return markdown;
  };

  const printPDF = (markdown: string) => {
    // Use a standard library or external service to print the Markdown document as a PDF
    // Example: print(markdown);
  };
  const renderList = (summaries: any) => {
    return (
      <Container maxWidth="lg">
        <Typography variant="h4" component="h2" sx={{ m: 2 }}>
          Video Summary:
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          sx={{ mb: 3 }}
          onClick={handlePrintPDF}
        >
          Print PDF of Data
        </Button>
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
                    {Object.keys(summary)}:
                  </Typography>
                  {summary[Object.keys(summary)[0]].summary}
                </ListItemButton>
              </ListItem>
            ))}
        </List>
      </Container>
    );
  };
  return (
    <Container maxWidth="lg">
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Box
              height={35}
              width={35}
              my={4}
              display="flex"
              alignItems="center"
              sx={{ mr: 2 }}
            >
              <img src={logo} alt="Logo" />
            </Box>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AI Youtube Summarizer
            </Typography>
            <Button color="inherit">Login</Button>
          </Toolbar>
        </AppBar>
      </Box>
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
            sx={{ mt: 4, mb: 3 }}
          >
            {loading ? <CircularProgress size={24} /> : "Summarize Now"}
          </Button>
        </form>
        {loading ? (
          <Typography variant="h6" sx={{ m: 2 }}>
            Enter a YouTube URL to summarize the video.
          </Typography>
        ) : (
          summaries && renderList(summaries)
        )}
        <ProTip />
        <Copyright />
      </Box>
    </Container>
  );
}
