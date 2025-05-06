import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider } from './contexts/AuthContext';
import theme from './utils/theme';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <BrowserRouter>
          <Navbar />
          <Routes>
            <Route path="/" element={<Navigate to="/products" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            
            {/* Rotas protegidas */}
            <Route 
              path="/cart" 
              element={
                <ProtectedRoute>
                  <Cart />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/checkout" 
              element={
                <ProtectedRoute>
                  <Checkout />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              } 
            />
            
            {/* Rota 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
          <Footer />
        </BrowserRouter>
        <ToastContainer position="bottom-right" />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
