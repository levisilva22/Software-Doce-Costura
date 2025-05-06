import { useState, useEffect } from 'react';
import { Grid, Typography, Box, Skeleton, Divider } from '@mui/material';
import { getTrendingProducts, getPersonalizedRecommendations } from '../../services/recommendationService';
import { useAuth } from '../../contexts/AuthContext';
import ProductCard from '../ProductCard';

const ProductRecommendations = ({ title = "Recomendados para você", maxItems = 4 }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated, user } = useAuth();

  useEffect(() => {
    async function fetchRecommendations() {
      try {
        setLoading(true);
        let recommendedProducts;
        
        if (isAuthenticated && user) {
          // Se o usuário está autenticado, buscar recomendações personalizadas
          recommendedProducts = await getPersonalizedRecommendations(user.id, maxItems);
        } else {
          // Caso contrário, mostrar produtos em tendência
          recommendedProducts = await getTrendingProducts(maxItems);
        }
        
        // Se as recomendações possuem apenas IDs de produtos, precisamos buscar os detalhes
        // Esta parte depende do formato de resposta da sua API
        if (recommendedProducts.length > 0 && typeof recommendedProducts[0] === 'object' 
            && recommendedProducts[0].product_id) {
          // Formatar os dados se necessário
          setProducts(recommendedProducts.map(item => ({
            id: item.product_id,
            score: item.score,
            // Aqui você pode adicionar mais campos se sua API retornar mais informações
            // ou pode precisar fazer outra chamada para buscar detalhes completos do produto
          })));
        } else {
          // Se já recebemos objetos completos de produtos
          setProducts(recommendedProducts);
        }
      } catch (error) {
        console.error('Erro ao buscar recomendações:', error);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    }

    fetchRecommendations();
  }, [isAuthenticated, user, maxItems]);

  if (loading) {
    return (
      <Box sx={{ mt: 4, mb: 2 }}>
        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
          {title}
        </Typography>
        <Grid container spacing={3}>
          {[...Array(4)].map((_, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Skeleton variant="rectangular" height={200} />
              <Skeleton height={30} width="80%" sx={{ mt: 1 }} />
              <Skeleton height={20} width="60%" />
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  if (products.length === 0) {
    return null;
  }

  return (
    <Box sx={{ mt: 4, mb: 2 }}>
      <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
        {title}
      </Typography>
      <Divider sx={{ mb: 3 }} />
      <Grid container spacing={3}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={3} key={product.id || product.product_id}>
            <ProductCard product={product} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ProductRecommendations;