// Crie este arquivo em /home/levi/E-commerce/frontend/src/pages/Profile.js
// eslint-disable-next-line no-unused-vars
import React from 'react';
import { Container, Typography, Box, Paper, Grid, Button } from '@mui/material';

function Profile() {
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Meu Perfil
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Informações Pessoais
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography><strong>Nome:</strong> Usuário Teste</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography><strong>Email:</strong> usuario@exemplo.com</Typography>
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" sx={{ mt: 2 }}>
              Editar Informações
            </Button>
          </Grid>
        </Grid>
      </Paper>
      
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Histórico de Pedidos
        </Typography>
        <Typography>
          Você ainda não realizou nenhum pedido.
        </Typography>
      </Paper>
    </Container>
  );
}

export default Profile;