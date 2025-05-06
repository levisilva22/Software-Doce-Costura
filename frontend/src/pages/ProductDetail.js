import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Button,
  Chip,
  Divider,
  Rating,
  TextField,
  Alert,
  Skeleton,
  Breadcrumbs,
  Link,
  Tabs,
  Tab,
} from '@mui/material';
import { ShoppingCart, Favorite, FavoriteBorder } from '@mui/icons-material';
import { getProductById } from '../services/productService';
import { getSimilarProducts } from '../services/recommendationService';
import { addToCart } from '../services/cartService';
import { useAuth } from '../contexts/AuthContext';
import { useInteractionTracker } from '../utils/interactionTracker';
import ProductCard from '../components/ProductCard';

function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { viewProduct, addToCart: trackAddToCart, favoriteProduct } = useInteractionTracker();
  
  const [product, setProduct] = useState(null);
  const [similarProducts, setSimilarProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [isFavorite, setIsFavorite] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [tabValue, setTabValue] = useState(0);
  
  useEffect(() => {
    const fetchProductDetails = async () => {
      setLoading(true);
      setErrorMessage('');
      try {
        // Busca detalhes do produto
        const productData = await getProductById(id);
        setProduct(productData);
        
        // Registra visualização do produto para o sistema de recomendação
        viewProduct(id);
        
        // Busca produtos similares como recomendação
        const similarData = await getSimilarProducts(id, 4);
        setSimilarProducts(similarData);
      } catch (error) {
        console.error('Erro ao buscar detalhes do produto:', error);
        setErrorMessage('Não foi possível carregar os detalhes do produto.');
      } finally {
        setLoading(false);
      }
    };
    
    if (id) {
      fetchProductDetails();
    }
  }, [id, viewProduct]);
  
  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value) || 1;
    const maxQuantity = product?.stock || 10;
    setQuantity(Math.min(Math.max(1, value), maxQuantity));
  };
  
  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    try {
      await addToCart(product.id, quantity);
      trackAddToCart(product.id, quantity);
      // Possível adição: mostrar uma notificação de sucesso
    } catch (error) {
      console.error('Erro ao adicionar ao carrinho:', error);
      setErrorMessage('Não foi possível adicionar o produto ao carrinho.');
    }
  };
  
  const handleToggleFavorite = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    setIsFavorite(!isFavorite);
    favoriteProduct(product.id, !isFavorite);
    // Possível adição: implementar favoritos no backend
  };
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ my: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Skeleton variant="rectangular" height={400} animation="wave" />
          </Grid>
          <Grid item xs={12} md={6}>
            <Skeleton variant="text" height={30} width="40%" />
            <Skeleton variant="text" height={60} width="90%" sx={{ mb: 2 }} />
            <Skeleton variant="text" height={30} width="30%" sx={{ mb: 1 }} />
            <Skeleton variant="text" height={50} width="50%" sx={{ mb: 3 }} />
            <Skeleton variant="rectangular" height={100} sx={{ mb: 3 }} />
            <Skeleton variant="rectangular" height={60} width="100%" />
          </Grid>
        </Grid>
      </Container>
    );
  }
  
  if (!product && !loading) {
    return (
      <Container maxWidth="lg" sx={{ my: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {errorMessage || 'Produto não encontrado'}
        </Alert>
        <Button
          variant="contained"
          onClick={() => navigate('/products')}
        >
          Voltar para produtos
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ my: 4 }}>
      {/* Breadcrumb */}
      <Breadcrumbs sx={{ mb: 3 }} aria-label="breadcrumb">
        <Link underline="hover" color="inherit" onClick={() => navigate('/')}>
          Home
        </Link>
        <Link underline="hover" color="inherit" onClick={() => navigate('/products')}>
          Produtos
        </Link>
        <Link
          underline="hover"
          color="inherit"
          onClick={() => navigate(`/products?category=${product.category_id}`)}
        >
          {product.category_name}
        </Link>
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>

      {errorMessage && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {errorMessage}
        </Alert>
      )}

      <Grid container spacing={4}>
        {/* Imagem do Produto */}
        <Grid item xs={12} md={6}>
          <Box 
            sx={{ 
              borderRadius: 2, 
              overflow: 'hidden',
              height: 400,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              bgcolor: '#f5f5f5'
            }}
          >
            <img 
              src={product.image || 'https://via.placeholder.com/500x500?text=Sem+Imagem'} 
              alt={product.name}
              style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
            />
          </Box>
        </Grid>

        {/* Detalhes do Produto */}
        <Grid item xs={12} md={6}>
          <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
              {product.category_name}
            </Typography>
            
            <Typography variant="h4" component="h1" sx={{ fontWeight: 700, mb: 2, mt: 1 }}>
              {product.name}
            </Typography>

            {/* Avaliações */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Rating value={product.rating || 0} precision={0.5} readOnly />
              <Typography variant="body2" sx={{ ml: 1 }}>
                ({product.rating_count || 0} avaliações)
              </Typography>
            </Box>

            {/* Preço */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Typography variant="h4" component="p" color="primary" sx={{ fontWeight: 700 }}>
                R$ {parseFloat(product.price).toFixed(2)}
              </Typography>
              {product.old_price && (
                <Typography
                  variant="body1"
                  sx={{ textDecoration: 'line-through', color: 'text.secondary' }}
                >
                  R$ {parseFloat(product.old_price).toFixed(2)}
                </Typography>
              )}
            </Box>

            {/* Descrição Curta */}
            <Typography variant="body1" sx={{ mb: 3 }}>
              {product.short_description || product.description}
            </Typography>

            <Divider sx={{ my: 2 }} />

            {/* Ações */}
            <Box sx={{ mt: 'auto', display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TextField
                  label="Quantidade"
                  type="number"
                  InputProps={{ inputProps: { min: 1, max: product.stock || 10 } }}
                  value={quantity}
                  onChange={handleQuantityChange}
                  sx={{ width: '100px' }}
                  size="small"
                />
                
                <Box sx={{ flexGrow: 1 }} />
                
                {product.stock > 0 ? (
                  <Chip 
                    label={`${product.stock} em estoque`} 
                    color="success" 
                    size="small" 
                  />
                ) : (
                  <Chip 
                    label="Fora de estoque" 
                    color="error" 
                    size="small" 
                  />
                )}
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  size="large"
                  startIcon={<ShoppingCart />}
                  fullWidth
                  onClick={handleAddToCart}
                  disabled={product.stock <= 0 || !isAuthenticated}
                >
                  {isAuthenticated ? 'Adicionar ao Carrinho' : 'Faça Login para Comprar'}
                </Button>
                
                <Button
                  variant="outlined"
                  color={isFavorite ? "error" : "primary"}
                  onClick={handleToggleFavorite}
                  sx={{ minWidth: 'auto', px: 2 }}
                  disabled={!isAuthenticated}
                >
                  {isFavorite ? <Favorite /> : <FavoriteBorder />}
                </Button>
              </Box>
            </Box>
          </Box>
        </Grid>
      </Grid>

      {/* Detalhes, Especificações, Avaliações */}
      <Box sx={{ mt: 6 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="product info tabs">
            <Tab label="Descrição" id="tab-0" />
            <Tab label="Especificações" id="tab-1" />
            <Tab label="Avaliações" id="tab-2" />
          </Tabs>
        </Box>
        <Box role="tabpanel" hidden={tabValue !== 0} sx={{ p: 3 }}>
          {tabValue === 0 && (
            <Typography variant="body1">
              {product.description || "Sem descrição detalhada disponível."}
            </Typography>
          )}
        </Box>
        <Box role="tabpanel" hidden={tabValue !== 1} sx={{ p: 3 }}>
          {tabValue === 1 && (
            product.specifications ? (
              <ul>
                {Object.entries(product.specifications).map(([key, value]) => (
                  <li key={key}>
                    <Typography component="span" fontWeight="bold">{key}:</Typography> {value}
                  </li>
                ))}
              </ul>
            ) : (
              <Typography>Sem especificações disponíveis.</Typography>
            )
          )}
        </Box>
        <Box role="tabpanel" hidden={tabValue !== 2} sx={{ p: 3 }}>
          {tabValue === 2 && (
            <Typography>Avaliações não disponíveis no momento.</Typography>
            // Aqui você pode implementar o componente de avaliações
          )}
        </Box>
      </Box>

      {/* Produtos Similares */}
      {similarProducts.length > 0 && (
        <Box sx={{ mt: 6 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
            Você também pode gostar
          </Typography>
          <Divider sx={{ mb: 3 }} />
          <Grid container spacing={3}>
            {similarProducts.map((product) => (
              <Grid item xs={12} sm={6} md={3} key={product.id}>
                <ProductCard product={product} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );
}

export default ProductDetail;