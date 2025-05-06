import { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container, InputBase, Badge, IconButton, Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import { ShoppingCart, Person, Search, Menu as MenuIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// Componente de busca estilizado
const SearchWrapper = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  border: '1px solid #ddd',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.primary.main,
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
}));

function Navbar() {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
      <Typography variant="h6" sx={{ my: 2, fontWeight: 700, color: 'primary.main' }}>
        Artesanato Shop
      </Typography>
      <Divider />
      <List>
        <ListItem button onClick={() => navigate('/products')}>
          <ListItemText primary="Produtos" />
        </ListItem>
        <ListItem button onClick={() => navigate('/categories')}>
          <ListItemText primary="Categorias" />
        </ListItem>
        <ListItem button onClick={() => navigate('/promotions')}>
          <ListItemText primary="Promoções" />
        </ListItem>
        {isAuthenticated ? (
          <>
            <ListItem button onClick={() => navigate('/cart')}>
              <ListItemText primary="Carrinho" />
            </ListItem>
            <ListItem button onClick={logout}>
              <ListItemText primary="Sair" />
            </ListItem>
          </>
        ) : (
          <ListItem button onClick={() => navigate('/login')}>
            <ListItemText primary="Login" />
          </ListItem>
        )}
      </List>
    </Box>
  );

  return (
    <AppBar position="sticky" elevation={0}>
      <Container maxWidth="lg">
        {/* Barra superior com logo */}
        <Toolbar disableGutters sx={{ 
          borderBottom: '1px solid #eaeaea',
          padding: { xs: '10px 0', md: '15px 0' }
        }}>
          <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
            >
              <MenuIcon />
            </IconButton>
          </Box>
          
          {/* Logo */}
          <Typography
            variant="h5"
            noWrap
            component="div"
            sx={{
              flexGrow: 1,
              cursor: 'pointer',
              fontWeight: 700,
              color: 'primary.main',
              letterSpacing: '0.5px',
              fontSize: { xs: '1.2rem', md: '1.5rem' }
            }}
            onClick={() => navigate('/products')}
          >
            Artesanato Shop
          </Typography>

          {/* Busca */}
          <SearchWrapper sx={{ display: { xs: 'none', md: 'block' } }}>
            <SearchIconWrapper>
              <Search />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Buscar produtos..."
              inputProps={{ 'aria-label': 'search' }}
            />
          </SearchWrapper>

          {/* Botões de ação */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', gap: 1 }}>
            {isAuthenticated ? (
              <>
                <Button
                  color="inherit"
                  startIcon={
                    <Badge badgeContent={4} color="error">
                      <ShoppingCart />
                    </Badge>
                  }
                  onClick={() => navigate('/cart')}
                  sx={{ borderRadius: '4px' }}
                >
                  Carrinho
                </Button>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={logout}
                  sx={{
                    borderRadius: '4px',
                    ml: 1
                  }}
                >
                  Sair
                </Button>
              </>
            ) : (
              <Button
                variant="contained"
                color="primary"
                startIcon={<Person />}
                onClick={() => navigate('/login')}
                sx={{ borderRadius: '4px' }}
              >
                Login
              </Button>
            )}
          </Box>
        </Toolbar>

        {/* Menu de categorias */}
        <Box 
          sx={{ 
            display: { xs: 'none', md: 'flex' },
            justifyContent: 'space-between',
            py: 1
          }}
        >
          {['Linha Casa', 'Papelaria', 'MDF', 'Pintura', 'Tecidos', 'Feltro', 'Biscuit'].map((item) => (
            <Button 
              key={item}
              color="inherit"
              sx={{ 
                fontSize: '0.9rem',
                fontWeight: 500,
                '&:hover': {
                  color: 'primary.main',
                  backgroundColor: 'transparent'
                }
              }}
            >
              {item}
            </Button>
          ))}
        </Box>
      </Container>

      {/* Drawer para mobile */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Melhor desempenho mobile
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
        }}
      >
        {drawer}
      </Drawer>
    </AppBar>
  );
}

export default Navbar;
