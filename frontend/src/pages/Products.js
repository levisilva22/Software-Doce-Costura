import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Divider,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  Skeleton,
  Pagination,
  TextField,
  InputAdornment
} from '@mui/material';
import { Search } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useInteractionTracker } from '../utils/interactionTracker';
import { getProducts, getCategories } from '../services/productService';
import { getTrendingProducts, getNewArrivals, getPersonalizedRecommendations } from '../services/recommendationService';
import ProductCard from '../components/ProductCard';

function Products() {
  // Hook de navegação
  const navigate = useNavigate();
  
  // Hooks de contexto
  const { isAuthenticated, user } = useAuth();
  const { searchProduct } = useInteractionTracker();
  
  // Estados
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('newest');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [newProducts, setNewProducts] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  
  // Carrega as categorias apenas uma vez
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (error) {
        console.error('Erro ao carregar categorias:', error);
      }
    };
    
    fetchCategories();
  }, []);

  // Carrega produtos principais com filtros
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const params = {
          page,
          limit: 12,
          sort_by: sortBy,
          category: selectedCategory || undefined,
          search: searchQuery || undefined
        };
        
        const data = await getProducts(params);
        setProducts(data.results || []);
        setTotalPages(data.total_pages || 1);
      } catch (error) {
        console.error('Erro ao carregar produtos:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, [page, sortBy, selectedCategory, searchQuery]);

  // Carrega produtos em tendência e novidades uma vez
  useEffect(() => {
    const fetchSpecialProducts = async () => {
      try {
        // Produtos em tendência
        const trending = await getTrendingProducts(4);
        setTrendingProducts(trending);

        // Novidades
        const newArrivals = await getNewArrivals(4);
        setNewProducts(newArrivals);
      } catch (error) {
        console.error('Erro ao carregar produtos especiais:', error);
      }
    };

    fetchSpecialProducts();
  }, []);

  // Carrega recomendações personalizadas se usuário estiver logado
  useEffect(() => {
    const fetchRecommendations = async () => {
      if (isAuthenticated && user?.id) {
        try {
          const recommendations = await getPersonalizedRecommendations(user.id, 4);
          setRecommendedProducts(recommendations);
        } catch (error) {
          console.error('Erro ao carregar recomendações:', error);
        }
      }
    };

    fetchRecommendations();
  }, [isAuthenticated, user]);
  
  // Funções de manipulação de eventos
  const handleSortChange = (event) => {
    setSortBy(event.target.value);
    setPage(1);
  };
  
  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setPage(1);
  };
  
  const handlePageChange = (event, value) => {
    setPage(value);
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };
  
  const handleSearch = (e) => {
    e.preventDefault();
    const query = e.target.search.value;
    setSearchQuery(query);
    setPage(1);
    
    // Rastreia a busca para o serviço de recomendação
    if (query) {
      searchProduct(query);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      {/* Cabeçalho e barra de busca */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
          flexDirection: { xs: 'column', sm: 'row' },
          gap: 2,
        }}
      >
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 700,
            color: 'primary.main'
          }}
        >
          Produtos para Artesanato
        </Typography>

        <Box component="form" onSubmit={handleSearch}>
          <TextField
            name="search"
            placeholder="Buscar produtos..."
            size="small"
            defaultValue={searchQuery}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </Box>
      </Box>

      {/* Filtros */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Categoria</InputLabel>
          <Select
            value={selectedCategory}
            label="Categoria"
            onChange={handleCategoryChange}
          >
            <MenuItem value="">Todas</MenuItem>
            {categories.map((category) => (
              <MenuItem key={category.id} value={category.id}>
                {category.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Ordenar por</InputLabel>
          <Select value={sortBy} label="Ordenar por" onChange={handleSortChange}>
            <MenuItem value="newest">Mais recentes</MenuItem>
            <MenuItem value="price_asc">Menor preço</MenuItem>
            <MenuItem value="price_desc">Maior preço</MenuItem>
            <MenuItem value="rating">Mais bem avaliados</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {/* Recomendações Personalizadas - mostra apenas se o usuário estiver logado e tiver recomendações */}
      {isAuthenticated && recommendedProducts.length > 0 && (
        <Box sx={{ mt: 4, mb: 6 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
            Recomendados para Você
          </Typography>
          <Divider sx={{ mb: 3 }} />
          <Grid container spacing={3}>
            {loading ? (
              Array.from(new Array(4)).map((_, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <Box sx={{ width: '100%', mb: 2 }}>
                    <Skeleton variant="rectangular" height={200} animation="wave" />
                    <Skeleton height={30} width="80%" sx={{ mt: 1 }} animation="wave" />
                    <Skeleton height={20} width="60%" animation="wave" />
                  </Box>
                </Grid>
              ))
            ) : (
              recommendedProducts.map((product) => (
                <Grid item xs={12} sm={6} md={3} key={product.id}>
                  <ProductCard product={product} />
                </Grid>
              ))
            )}
          </Grid>
        </Box>
      )}

      {/* Produtos em Tendência */}
      <Box sx={{ mt: 6, mb: 2 }}>
        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
          Em Tendência
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Grid container spacing={3}>
          {loading ? (
            Array.from(new Array(4)).map((_, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Box sx={{ width: '100%', mb: 2 }}>
                  <Skeleton variant="rectangular" height={200} animation="wave" />
                  <Skeleton height={30} width="80%" sx={{ mt: 1 }} animation="wave" />
                  <Skeleton height={20} width="60%" animation="wave" />
                </Box>
              </Grid>
            ))
          ) : (
            trendingProducts.map((product) => (
              <Grid item xs={12} sm={6} md={3} key={product.id}>
                <ProductCard product={product} />
              </Grid>
            ))
          )}
        </Grid>
      </Box>

      {/* Novidades */}
      <Box sx={{ mt: 6, mb: 2 }}>
        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
          Novidades
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Grid container spacing={3}>
          {loading ? (
            Array.from(new Array(4)).map((_, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Box sx={{ width: '100%', mb: 2 }}>
                  <Skeleton variant="rectangular" height={200} animation="wave" />
                  <Skeleton height={30} width="80%" sx={{ mt: 1 }} animation="wave" />
                  <Skeleton height={20} width="60%" animation="wave" />
                </Box>
              </Grid>
            ))
          ) : (
            newProducts.map((product) => (
              <Grid item xs={12} sm={6} md={3} key={product.id}>
                <ProductCard product={product} />
              </Grid>
            ))
          )}
        </Grid>
      </Box>

      {/* Lista Principal de Produtos */}
      <Box sx={{ mt: 6 }}>
        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
          {searchQuery ? `Resultados para: "${searchQuery}"` : "Todos os Produtos"}
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Grid container spacing={3}>
          {loading ? (
            Array.from(new Array(8)).map((_, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Box sx={{ width: '100%', mb: 2 }}>
                  <Skeleton variant="rectangular" height={200} animation="wave" />
                  <Skeleton height={30} width="80%" sx={{ mt: 1 }} animation="wave" />
                  <Skeleton height={20} width="60%" animation="wave" />
                </Box>
              </Grid>
            ))
          ) : products.length > 0 ? (
            products.map((product) => (
              <Grid item xs={12} sm={6} md={3} key={product.id}>
                <ProductCard product={product} />
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Box sx={{ textAlign: 'center', py: 5 }}>
                <Typography variant="h6" color="text.secondary">
                  Nenhum produto encontrado
                </Typography>
              </Box>
            </Grid>
          )}
        </Grid>
        
        {/* Paginação */}
        {totalPages > 1 && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <Pagination 
              count={totalPages} 
              page={page} 
              onChange={handlePageChange} 
              color="primary"
            />
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default Products;
