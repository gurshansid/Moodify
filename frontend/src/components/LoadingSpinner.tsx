import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-white/30 rounded-full animate-spin border-t-white">
        </div>
        <div className="absolute inset-0 w-16 h-16 border-4 border-transparent rounded-full animate-pulse border-l-white/50">
        </div>
      </div>
      <p className="mt-4 text-white/80 animate-pulse">
        Finding perfect songs for your mood...
      </p>
    </div>
  );
};

export default LoadingSpinner;