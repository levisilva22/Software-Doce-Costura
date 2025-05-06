// Crie este arquivo em /home/levi/E-commerce/frontend/src/pages/NotFound.js
import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <Container maxWidth="sm" sx={{ textAlign: 'center', my: 8 }}>
      <Typography variant="h1" component="h1" sx={{ mb: 2, fontWeight: 700, fontSize: '8rem', color: 'primary.main' }}>
        404
      </Typography>
      
      <Typography variant="h4" component="h2" sx={{ mb: 4 }}>
        Página não encontrada
      </Typography>
      
      <Typography variant="body1" sx={{ mb: 4 }}>
        A página que você está procurando não existe ou foi movida.
      </Typography>
      
      <Box>
        <Button 
          component={Link} 
          to="/" 
          variant="contained" 
          color="primary" 
          size="large"
        >
          Voltar para a página inicial
        </Button>
      </Box>
    </Container>
  );
}

export default NotFound;