import React from 'react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">Welcome to your Dashboard!</h1>
      <p className="text-lg mb-8">You are logged in.</p>
      <Button onClick={handleLogout}>Logout</Button>
    </div>
  );
};

export default DashboardPage;