import { useState, useRef, useEffect } from 'react';
import {
  Box, Paper, TextField, IconButton, List, ListItem, Avatar, Divider, Card, CardContent
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

import { Typography, Button } from '../../components/atoms';
import { sendMessageApi } from '../../api/chatbot';

export function Chatbot() {
  const [messages, setMessages] = useState([
    {
      tipo: 'bot',
      mensaje: '¡Hola! Soy el asistente virtual de Emily Tech. Puedo ayudarte con información sobre nuestra empresa, productos y servicios. ¿En qué puedo ayudarte hoy?',
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
          mensaje: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
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

  const handleSugerencia = async (sugerencia) => {
    if (loading) return;

    setMessages((prev) => [...prev, { tipo: 'user', mensaje: sugerencia }]);
    setLoading(true);

    try {
      const response = await sendMessageApi(sugerencia, sessionId);

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
          mensaje: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const sugerencias = [
    '¿Dónde está ubicada Emily Tech?',
    '¿Qué servicios ofrecen?',
    '¿Cuáles son los horarios de atención?',
    '¿Cómo puedo contactarlos?',
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Chatbot IA
      </Typography>
      <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
        Asistente virtual inteligente
      </Typography>

      <Box sx={{ display: 'flex', gap: 3, flexDirection: { xs: 'column', md: 'row' } }}>
        {/* Chat principal */}
        <Paper
          elevation={3}
          sx={{
            flex: 1,
            height: 500,
            display: 'flex',
            flexDirection: 'column',
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
            <Typography variant="h6">Emily Tech Assistant</Typography>
          </Box>

          {/* Messages */}
          <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2, bgcolor: '#f5f5f5' }}>
            <List>
              {messages.map((msg, index) => (
                <ListItem
                  key={index}
                  sx={{
                    flexDirection: msg.tipo === 'user' ? 'row-reverse' : 'row',
                    gap: 1,
                    alignItems: 'flex-start',
                    py: 1,
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: msg.tipo === 'user' ? 'secondary.main' : 'primary.main',
                      width: 40,
                      height: 40,
                    }}
                  >
                    {msg.tipo === 'user' ? <PersonIcon /> : <SmartToyIcon />}
                  </Avatar>
                  <Paper
                    elevation={1}
                    sx={{
                      p: 2,
                      maxWidth: '70%',
                      bgcolor: msg.tipo === 'user' ? 'secondary.light' : 'white',
                      color: msg.tipo === 'user' ? 'white' : 'text.primary',
                      borderRadius: 2,
                    }}
                  >
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {msg.mensaje}
                    </Typography>
                  </Paper>
                </ListItem>
              ))}
              {loading && (
                <ListItem sx={{ gap: 1, alignItems: 'flex-start' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 40, height: 40 }}>
                    <SmartToyIcon />
                  </Avatar>
                  <Paper sx={{ p: 2, borderRadius: 2 }}>
                    <Typography variant="body2" color="textSecondary">
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
          <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              placeholder="Escribe tu mensaje..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              multiline
              maxRows={3}
            />
            <IconButton
              color="primary"
              onClick={handleSend}
              disabled={loading || !input.trim()}
              sx={{ alignSelf: 'flex-end' }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Paper>

        {/* Sugerencias */}
        <Card sx={{ width: { xs: '100%', md: 300 } }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Sugerencias
            </Typography>
            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
              Prueba preguntando:
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {sugerencias.map((sugerencia, index) => (
                <Button
                  key={index}
                  variant="outlined"
                  size="small"
                  onClick={() => handleSugerencia(sugerencia)}
                  disabled={loading}
                  sx={{ textTransform: 'none', justifyContent: 'flex-start' }}
                >
                  {sugerencia}
                </Button>
              ))}
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}
