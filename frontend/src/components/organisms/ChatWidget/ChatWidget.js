import { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Fab,
  Collapse,
  TextField,
  IconButton,
  List,
  ListItem,
  Avatar,
  Divider,
  Typography,
} from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import { sendMessageApi } from '../../../api/chatbot';

export function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      tipo: 'bot',
      mensaje: '¡Hola! Soy el asistente de Emily Tech. ¿En qué puedo ayudarte?',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');

    setMessages((prev) => [...prev, { tipo: 'user', mensaje: userMessage }]);
    setLoading(true);

    try {
      const response = await sendMessageApi(userMessage, sessionId);

      if (response.session_id) {
        setSessionId(response.session_id);
      }

      setMessages((prev) => [
        ...prev,
        { tipo: 'bot', mensaje: response.response || 'Sin respuesta' },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          tipo: 'bot',
          mensaje: 'Lo siento, hubo un error. Por favor, intenta de nuevo.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <Fab
        color="primary"
        onClick={() => setOpen(!open)}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          zIndex: 1000,
        }}
      >
        {open ? <CloseIcon /> : <ChatIcon />}
      </Fab>

      <Collapse in={open}>
        <Paper
          elevation={8}
          sx={{
            position: 'fixed',
            bottom: 90,
            right: 24,
            width: 350,
            height: 450,
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          {/* Header */}
          <Box
            sx={{
              bgcolor: 'primary.main',
              color: 'white',
              p: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <SmartToyIcon />
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
              Chatbot IA
            </Typography>
          </Box>

          {/* Messages */}
          <Box
            sx={{
              flexGrow: 1,
              overflow: 'auto',
              p: 2,
              bgcolor: '#f5f5f5',
            }}
          >
            <List>
              {messages.map((msg, index) => (
                <ListItem
                  key={index}
                  sx={{
                    flexDirection: msg.tipo === 'user' ? 'row-reverse' : 'row',
                    gap: 1,
                    alignItems: 'flex-start',
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: msg.tipo === 'user' ? 'secondary.main' : 'primary.main',
                      width: 32,
                      height: 32,
                    }}
                  >
                    {msg.tipo === 'user' ? <PersonIcon fontSize="small" /> : <SmartToyIcon fontSize="small" />}
                  </Avatar>
                  <Paper
                    sx={{
                      p: 1.5,
                      maxWidth: '70%',
                      bgcolor: msg.tipo === 'user' ? 'secondary.light' : 'white',
                    }}
                  >
                    <Typography
                      variant="body2"
                      sx={{ color: msg.tipo === 'user' ? 'white' : 'text.primary' }}
                    >
                      {msg.mensaje}
                    </Typography>
                  </Paper>
                </ListItem>
              ))}
              {loading && (
                <ListItem>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                    <SmartToyIcon fontSize="small" />
                  </Avatar>
                  <Paper sx={{ p: 1.5, ml: 1 }}>
                    <Typography variant="body2" color="text.primary">
                      Escribiendo...
                    </Typography>
                  </Paper>
                </ListItem>
              )}
              <div ref={messagesEndRef} />
            </List>
          </Box>

          <Divider />

          {/* Input */}
          <Box sx={{ p: 1, display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Escribe tu mensaje..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <IconButton color="primary" onClick={handleSend} disabled={loading || !input.trim()}>
              <SendIcon />
            </IconButton>
          </Box>
        </Paper>
      </Collapse>
    </>
  );
}
