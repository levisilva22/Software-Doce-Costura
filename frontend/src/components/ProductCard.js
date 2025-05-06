import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip,
  IconButton,
  Rating,
  Tooltip,
} from '@mui/material';
import { ShoppingCart, FavoriteBorder, Favorite } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useInteractionTracker } from '../utils/interactionTracker';
import { addToCart } from '../services/cartService';

const ProductCard = ({ product }) => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { viewProduct, clickProduct, addToCart: trackAddToCart, favoriteProduct } = useInteractionTracker();
  const [isFavorite, setIsFavorite] = useState(false);

  // Registrar visualização quando o componente é montado
  useEffect(() => {
    viewProduct(product.id);
  }, [product.id, viewProduct]);

  const handleCardClick = () => {
    clickProduct(product.id);
    navigate(`/products/${product.id}`);
  };

  const handleAddToCart = async (e) => {
    e.stopPropagation(); // Evita propagar o clique para o card
    
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    try {
      await addToCart(product.id, 1);
      trackAddToCart(product.id, 1);
    } catch (error) {
      console.error('Erro ao adicionar ao carrinho:', error);
    }
  };

  const handleToggleFavorite = (e) => {
    e.stopPropagation(); // Evita propagar o clique para o card
    
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    const newState = !isFavorite;
    setIsFavorite(newState);
    favoriteProduct(product.id, newState);
  };

  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        cursor: 'pointer'
      }}
      onClick={handleCardClick}
    >
      <Box sx={{ position: 'relative', pt: 2, px: 2 }}>
        {product.tag && (
          <Chip
            label={product.tag}
            color={
              product.tag === 'Promoção' ? 'error' : 
              product.tag === 'Mais Vendido' ? 'secondary' : 
              'primary'
            }
            sx={{
              position: 'absolute',
              top: 10,
              left: 10,
              zIndex: 1,
              fontWeight: 'bold',
            }}
            size="small"
          />
        )}

        <IconButton 
          sx={{ 
            position: 'absolute', 
            top: 5, 
            right: 5,
            zIndex: 1,
            color: isFavorite ? 'error.main' : 'action.disabled',
            bgcolor: 'rgba(255,255,255,0.8)',
          }}
          onClick={handleToggleFavorite}
          aria-label={isFavorite ? "Remover dos favoritos" : "Adicionar aos favoritos"}
        >
          {isFavorite ? <Favorite /> : <FavoriteBorder />}
        </IconButton>

        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center',
            height: 200,
            overflow: 'hidden',
            borderRadius: 2,
          }}
        >
          <CardMedia
            component="img"
            image={product.image || 'https://via.placeholder.com/300x300?text=Sem+Imagem'}
            alt={product.name}
            sx={{ 
              height: '100%', 
              objectFit: 'cover',
              transition: 'transform 0.3s ease',
            }}
          />
        </Box>
      </Box>

      <CardContent sx={{ flexGrow: 1, pt: 2 }}>
        <Typography 
          variant="caption" 
          color="text.secondary"
          sx={{ textTransform: 'uppercase', fontWeight: 500 }}
        >
          {product.category_name || product.category}
        </Typography>
        
        <Typography 
          gutterBottom 
          variant="h6" 
          component="h2" 
          sx={{ 
            fontWeight: 600,
            fontSize: '1rem',
            height: '2.5rem',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {product.name}
        </Typography>

        {product.rating !== undefined && (
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Rating value={product.rating} precision={0.5} size="small" readOnly />
            <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
              ({product.rating})
            </Typography>
          </Box>
        )}

        <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1, mt: 1 }}>
          {product.old_price && (
            <Typography 
              variant="body2" 
              sx={{ 
                textDecoration: 'line-through',
                color: 'text.secondary'
              }}
            >
              R$ {parseFloat(product.old_price).toFixed(2)}
            </Typography>
          )}
          <Typography 
            variant="h6" 
            component="span" 
            sx={{ 
              fontWeight: 700,
              color: product.old_price ? 'error.main' : 'primary.main'
            }}
          >
            R$ {parseFloat(product.price).toFixed(2)}
          </Typography>
        </Box>
        
        {product.stock !== undefined && product.stock < 10 && (
          <Typography 
            variant="caption" 
            sx={{ 
              color: product.stock < 5 ? 'error.main' : 'warning.main',
              fontWeight: 500,
              display: 'block',
              mt: 1
            }}
          >
            {product.stock < 5 ? `Apenas ${product.stock} em estoque!` : `${product.stock} unidades em estoque`}
          </Typography>
        )}
      </CardContent>

      <CardActions sx={{ px: 2, pb: 2 }}>
        <Tooltip title={!isAuthenticated ? "Faça login para comprar" : ""}>
          <span style={{ width: '100%' }}>
            <Button 
              variant="contained" 
              color="primary" 
              fullWidth
              startIcon={<ShoppingCart />}
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              sx={{ 
                py: 1,
                boxShadow: 'none',
                '&:hover': { boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }
              }}
            >
              Adicionar ao Carrinho
            </Button>
          </span>
        </Tooltip>
      </CardActions>
    </Card>
  );
};

export default ProductCard;