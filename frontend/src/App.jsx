import { Box, Paper, Typography, Stack, Fab } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState, useCallback } from 'react';
import { Mic } from '@mui/icons-material';
import VoiceRecordingDialog from './components/VoiceRecordingDialog';

function useCategories() {
  const [categories, setCategories] = useState([]);

  const fetchCategories = useCallback(async () => {
    try {
      const res = await fetch('http://localhost:8000/categories');
      const data = await res.json();
      setCategories(data);
    } catch (err) {
      setCategories([]);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  return { categories, fetchCategories };
}

function CategoryList() {
  const { categories, fetchCategories } = useCategories();
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleTaskCreated = (newTask) => {
    // After a new task is created, refresh categories from backend
    fetchCategories();
    setDialogOpen(false);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#111', py: 6, position: 'relative' }}>
      <Stack spacing={6} alignItems="center">
        {categories.map((cat) => (
          <Link
            key={cat.id}
            to={`/category/${cat.id}`}
            style={{ textDecoration: 'none', width: '100%' }}
          >
            <Box display="flex" alignItems="flex-start" gap={4} width={{ xs: '95%', sm: '80%', md: '60%' }} sx={{ cursor: 'pointer', transition: 'box-shadow 0.2s', '&:hover': { boxShadow: 6 } }}>
              <Paper
                elevation={3}
                sx={{
                  width: 220,
                  height: 150,
                  overflow: 'hidden',
                  borderRadius: 4,
                  flexShrink: 0,
                  background: 'none',
                }}
              >
                <img
                  src={cat.image}
                  alt={cat.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 16 }}
                />
              </Paper>
              <Box flex={1}>
                <Typography variant="h5" fontWeight={700} color="#fff" gutterBottom>
                  {cat.title}
                </Typography>
                <Typography variant="body2" color="#bdbdbd">
                  {cat.tasks.length} tasks
                </Typography>
              </Box>
            </Box>
          </Link>
        ))}
      </Stack>

      {/* Floating Action Button for Add Task */}
      <Fab
        color="primary"
        aria-label="add task"
        onClick={() => setDialogOpen(true)}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          bgcolor: '#2196f3',
          '&:hover': { bgcolor: '#1976d2' }
        }}
      >
        <Mic />
      </Fab>

      {/* Voice Recording Dialog */}
      <VoiceRecordingDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onTaskCreated={handleTaskCreated}
      />
    </Box>
  );
}

function CategoryTasks() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { categories, fetchCategories } = useCategories();
  const [dialogOpen, setDialogOpen] = useState(false);
  const cat = categories.find((c) => c.id === id);
  
  if (!cat) return <Box sx={{ color: '#fff', p: 4 }}>Category not found.</Box>;
  
  const handleTaskCreated = (newTask) => {
    // After a new task is created, refresh categories from backend
    fetchCategories();
    setDialogOpen(false);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#111', py: 6, position: 'relative' }}>
      <Box width={{ xs: '95%', sm: '80%', md: '60%' }} mx="auto">
        <Box display="flex" alignItems="center" gap={2} mb={4}>
          <Paper
            elevation={3}
            sx={{
              width: 120,
              height: 80,
              overflow: 'hidden',
              borderRadius: 4,
              flexShrink: 0,
              background: 'none',
            }}
          >
            <img
              src={cat.image}
              alt={cat.title}
              style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 12 }}
            />
          </Paper>
          <Typography variant="h5" fontWeight={700} color="#fff">
            {cat.title}
          </Typography>
          <Box flex={1} />
          <Typography
            variant="body2"
            color="#bdbdbd"
            sx={{ cursor: 'pointer', textDecoration: 'underline' }}
            onClick={() => navigate(-1)}
          >
            Back
          </Typography>
        </Box>
        <Stack spacing={2}>
          {cat.tasks.map((task, i) => (
            <Paper key={i} elevation={2} sx={{ p: 2, bgcolor: '#181818', color: '#fff' }}>
              <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                {task.title}
              </Typography>
              <Typography variant="body2" color="#bdbdbd">
                Assigned to: {task.assignee} &nbsp;|&nbsp; Due: {task.deadline}
              </Typography>
              <Typography variant="body2" color="#bdbdbd" mt={1}>
                {task.description}
              </Typography>
            </Paper>
          ))}
        </Stack>
      </Box>

      {/* Floating Action Button for Add Task */}
      <Fab
        color="primary"
        aria-label="add task"
        onClick={() => setDialogOpen(true)}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          bgcolor: '#2196f3',
          '&:hover': { bgcolor: '#1976d2' }
        }}
      >
        <Mic />
      </Fab>

      {/* Voice Recording Dialog */}
      <VoiceRecordingDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onTaskCreated={handleTaskCreated}
      />
    </Box>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CategoryList />} />
        <Route path="/category/:id" element={<CategoryTasks />} />
      </Routes>
    </Router>
  );
}
