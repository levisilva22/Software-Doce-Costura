import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  getPersonalizedRecommendations, 
  getTrendingProducts 
} from '../services/recommendationService';
import { Box, Typography, Grid, CircularProgress } from '@mui/material';
import ProductCard from './ProductCard'; // Seu componente de card de produto

function RecommendedProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated, user } = useAuth();

  useEffect(() => {
    async function loadRecommendations() {
      try {
        setLoading(true);
        let recommendedProducts;

        if (isAuthenticated) {
          // Se o usuário está logado, obter recomendações personalizadas
          recommendedProducts = await getPersonalizedRecommendations(8);
        } else {
          // Se não, mostrar produtos em tendência
          recommendedProducts = await getTrendingProducts(8);
        }

        setProducts(recommendedProducts);
      } catch (error) {
        console.error('Erro ao carregar recomendações:', error);
      } finally {
        setLoading(false);
      }
    }

    loadRecommendations();
  }, [isAuthenticated, user]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ my: 4 }}>
      <Typography 
        variant="h5" 
        component="h2" 
        sx={{ mb: 3, fontWeight: 600, color: 'primary.main' }}
      >
        {isAuthenticated 
          ? 'Recomendados para Você' 
          : 'Produtos em Destaque'}
      </Typography>
      <Grid container spacing={3}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={3} key={product.product_id}>
            <ProductCard product={product} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default RecommendedProducts;