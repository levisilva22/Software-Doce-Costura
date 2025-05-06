import React from 'react';
import { Container, Typography, List, ListItem, Button, Box } from '@mui/material';

function Cart() {
  return (
    <Container>
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Meu Carrinho
      </Typography>
      <List>
        {/* Conteúdo do carrinho será implementado posteriormente */}
        <ListItem>
          <Typography>O carrinho está vazio</Typography>
        </ListItem>
      </List>
      <Box sx={{ mt: 2 }}>
        <Button variant="contained" color="primary">
          Finalizar Compra
        </Button>
      </Box>
    </Container>
  );
}

export default Cart;
