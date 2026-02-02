import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div>
        <h1 className="text-4xl font-bold mb-4">Welcome to Corexus!</h1>
        <p className="text-lg">This is the home page. <Link to="/login" className="text-blue-500 hover:underline">Login here</Link>.</p>
      </div>
    </div>
  );
};

export default HomePage;