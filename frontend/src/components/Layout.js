import React from 'react';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Layout({ children }) {
  const { signed, logout } = useAuth();

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            E-Commerce
          </Typography>
          <Button color="inherit" component={RouterLink} to="/">
            Produtos
          </Button>
          {signed ? (
            <>
              <Button color="inherit" component={RouterLink} to="/cart">
                Carrinho
              </Button>
              <Button color="inherit" onClick={logout}>
                Sair
              </Button>
            </>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login">
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>
        {children}
      </Container>
    </>
  );
}

export default Layout;
