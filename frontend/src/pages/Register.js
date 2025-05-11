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
import { Visibility, VisibilityOff, Email, Lock, Person } from '@mui/icons-material';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Validação básica
    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }
    
    setLoading(true);

    try {
      // Utiliza a função register do contexto que já está integrada ao microserviço
      await register({
        name: formData.name,
        email: formData.email,
        password: formData.password
      });
      
      // Redireciona para a página de login após cadastro bem-sucedido
      navigate('/login');
    } catch (err) {
      console.error('Erro de cadastro:', err);
      
      // Tratamento de erros do microserviço de autenticação
      if (err.response) {
        if (err.response.status === 400) {
          setError('Email já cadastrado ou dados inválidos');
        } else if (err.response.data && err.response.data.message) {
          setError(err.response.data.message);
        } else {
          setError('Erro ao fazer cadastro. Por favor, tente novamente.');
        }
      } else if (err.request) {
        setError('Não foi possível conectar ao servidor. Verifique sua conexão.');
      } else {
        setError('Erro ao processar requisição de cadastro.');
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
            Criar Conta
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Preencha os campos abaixo para se cadastrar
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
            label="Nome completo"
            name="name"
            margin="normal"
            required
            value={formData.name}
            onChange={handleChange}
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Person color="primary" />
                </InputAdornment>
              ),
            }}
          />
          
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            margin="normal"
            required
            value={formData.email}
            onChange={handleChange}
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
            name="password"
            margin="normal"
            type={showPassword ? 'text' : 'password'}
            required
            value={formData.password}
            onChange={handleChange}
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
          
          <TextField
            fullWidth
            label="Confirmar senha"
            name="confirmPassword"
            margin="normal"
            type={showPassword ? 'text' : 'password'}
            required
            value={formData.confirmPassword}
            onChange={handleChange}
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock color="primary" />
                </InputAdornment>
              ),
            }}
          />
          
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
            ) : 'Cadastrar'}
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
                onClick={() => navigate('/login')}
                disabled={loading}
              >
                Já tenho uma conta
              </Button>
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Ao se cadastrar, você concorda com nossos 
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

export default Register;
