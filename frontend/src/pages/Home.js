import { Container, Typography, Box, Grid } from '@mui/material';
import RecommendedProducts from '../components/RecommendedProducts';
import { getNewArrivals, getTrendingProducts } from '../services/recommendationService';
import { useState, useEffect } from 'react';
import ProductCard from '../components/ProductCard';

function Home() {
  const [newProducts, setNewProducts] = useState([]);
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHomeData() {
      try {
        setLoading(true);
        
        // Carregar dados em paralelo
        const [newData, trendingData] = await Promise.all([
          getNewArrivals(4),
          getTrendingProducts(4)
        ]);
        
        setNewProducts(newData);
        setTrendingProducts(trendingData);
      } catch (error) {
        console.error('Erro ao carregar dados da página inicial:', error);
      } finally {
        setLoading(false);
      }
    }
    
    loadHomeData();
  }, []);

  return (
    <Container maxWidth="lg">
      {/* Banner principal */}
      <Box sx={{ my: 4 }}>
        {/* Banner com promoções */}
      </Box>
      
      {/* Recomendações personalizadas */}
      <RecommendedProducts />
      
      {/* Novos produtos */}
      <Box sx={{ my: 4 }}>
        <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
          Novidades
        </Typography>
        <Grid container spacing={3}>
          {newProducts.map((product) => (
            <Grid item xs={12} sm={6} md={3} key={product.product_id}>
              <ProductCard product={product} />
            </Grid>
          ))}
        </Grid>
      </Box>
      
      {/* Produtos em tendência */}
      <Box sx={{ my: 4 }}>
        <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
          Mais Populares
        </Typography>
        <Grid container spacing={3}>
          {trendingProducts.map((product) => (
            <Grid item xs={12} sm={6} md={3} key={product.product_id}>
              <ProductCard product={product} />
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default Home;