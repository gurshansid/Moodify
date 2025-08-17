import React, { useState } from 'react';
import MoodInput from './components/MoodInput';
import TrackList from './components/TrackList';
import LoadingSpinner from './components/LoadingSpinner';
import { api } from './services/api.js';
import type { RecommendationResponse } from './types';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleMoodSubmit = async (mood: string) => {
    setIsLoading(true);
    setError(null);
    setRecommendations(null);

    try {
      const response = await api.getRecommendations({ mood, limit: 10 });
      setRecommendations(response);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('API Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSearch = () => {
    setRecommendations(null);
    setError(null);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto">
        {!recommendations && !isLoading && (
          <MoodInput onSubmit={handleMoodSubmit} isLoading={isLoading} />
        )}

        {isLoading && <LoadingSpinner />}

        {error && (
          <div className="glass-effect rounded-xl p-6 max-w-2xl mx-auto text-center">
            <div className="text-red-300 text-xl mb-4">
              ❌ {error}
            </div>
            <button
              onClick={handleNewSearch}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Try Again
            </button>
          </div>
        )}

        {recommendations && (
          <TrackList data={recommendations} onNewSearch={handleNewSearch} />
        )}
      </div>
    </div>
  );
}

export default App;