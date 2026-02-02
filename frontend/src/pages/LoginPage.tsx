import React from 'react';

const LoginPage: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="p-8 border rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        {/* Login form will go here */}
        <p className="text-center text-sm text-gray-600">
          This is the login page.
        </p>
      </div>
    </div>
  );
};

export default LoginPage;