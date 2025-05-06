import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Divider,
  Link,
  Grid,
  InputAdornment,
  IconButton,
  CircularProgress,
} from '@mui/material';
import { Visibility, VisibilityOff, Email, Lock } from '@mui/icons-material';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Utiliza a função login do contexto que já está integrada ao microserviço
      await login({ email, password });
      
      // Redireciona para a página de produtos
      navigate('/products');
    } catch (err) {
      console.error('Erro de login:', err);
      
      // Tratamento de erros do microserviço de autenticação
      if (err.response) {
        // O servidor respondeu com um código de status fora do intervalo 2xx
        if (err.response.status === 401) {
          setError('Email ou senha incorretos');
        } else if (err.response.data && err.response.data.message) {
          setError(err.response.data.message);
        } else {
          setError('Erro ao fazer login. Por favor, tente novamente.');
        }
      } else if (err.request) {
        // A requisição foi feita mas não houve resposta
        setError('Não foi possível conectar ao servidor. Verifique sua conexão.');
      } else {
        // Algo aconteceu na configuração da requisição que gerou o erro
        setError('Erro ao processar requisição de login.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8, mb: 8 }}>
      <Paper elevation={3} sx={{ p: { xs: 3, md: 5 }, borderRadius: 2 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography 
            variant="h4" 
            component="h1" 
            color="primary.main"
            sx={{ fontWeight: 700 }}
          >
            Bem-vindo(a)
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Faça login para acessar sua conta
          </Typography>
        </Box>
        
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            fullWidth
            label="Email"
            margin="normal"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Email color="primary" />
                </InputAdornment>
              ),
            }}
          />
          
          <TextField
            fullWidth
            label="Senha"
            margin="normal"
            type={showPassword ? 'text' : 'password'}
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock color="primary" />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    edge="end"
                    disabled={loading}
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
          
          <Box sx={{ textAlign: 'right', mt: 1 }}>
            <Link href="#" variant="body2" underline="hover">
              Esqueceu a senha?
            </Link>
          </Box>
          
          <Button
            fullWidth
            variant="contained"
            color="primary"
            size="large"
            type="submit"
            disabled={loading}
            sx={{ 
              mt: 3, 
              py: 1.5,
              fontSize: '1rem',
              boxShadow: '0 4px 12px rgba(255, 107, 0, 0.3)',
              position: 'relative'
            }}
          >
            {loading ? (
              <CircularProgress 
                size={24} 
                color="inherit" 
                sx={{ position: 'absolute' }} 
              />
            ) : 'Entrar'}
          </Button>
          
          <Divider sx={{ my: 4 }}>
            <Typography variant="body2" color="text.secondary">
              Ou
            </Typography>
          </Divider>
          
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Button 
                fullWidth 
                variant="outlined" 
                color="primary"
                sx={{ py: 1 }}
                onClick={() => navigate('/register')}
                disabled={loading}
              >
                Cadastre-se
              </Button>
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Ao acessar, você concorda com nossos 
              <Link href="#" underline="hover" sx={{ ml: 0.5 }}>
                Termos de Uso
              </Link>
              {' '}e{' '}
              <Link href="#" underline="hover">
                Política de Privacidade
              </Link>
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default Login;
