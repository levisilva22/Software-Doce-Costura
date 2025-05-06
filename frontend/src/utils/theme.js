import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#ff6b00', // Laranja vibrante como no site de referência
      light: '#ff954d',
      dark: '#cc5500',
      contrastText: '#fff',
    },
    secondary: {
      main: '#28a745', // Verde para botões de ação
      light: '#48c267',
      dark: '#1e7e34',
      contrastText: '#fff',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
    text: {
      primary: '#333333',
      secondary: '#6c757d',
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h4: {
      fontWeight: 700,
      fontSize: '1.75rem',
      marginBottom: '1rem',
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
    },
    button: {
      textTransform: 'none', // Evita texto todo em maiúsculas nos botões
      fontWeight: 600,
    },
  },
  components: {
    MuiContainer: {
      styleOverrides: {
        root: {
          paddingTop: '1.5rem',
          paddingBottom: '2rem',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          padding: '8px 16px',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          },
        },
        containedPrimary: {
          backgroundImage: 'linear-gradient(135deg, #ff6b00 0%, #ff954d 100%)',
        },
        containedSecondary: {
          backgroundImage: 'linear-gradient(135deg, #28a745 0%, #48c267 100%)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 3px 10px rgba(0,0,0,0.08)',
          transition: 'transform 0.3s ease, box-shadow 0.3s ease',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          backgroundColor: '#fff',
          color: '#333',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
        colorPrimary: {
          backgroundColor: '#ff6b00',
        },
      },
    },
  },
});

export default theme;