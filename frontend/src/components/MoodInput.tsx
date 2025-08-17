import React, { useState } from 'react';

interface MoodInputProps {
  onSubmit: (mood: string) => void;
  isLoading: boolean;
}

const MoodInput: React.FC<MoodInputProps> = ({ onSubmit, isLoading }) => {
  const [mood, setMood] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (mood.trim() && !isLoading) {
      onSubmit(mood.trim());
    }
  };

  const moodSuggestions = [
    'Happy and energetic',
    'Sad and melancholic',
    'Relaxed and chill',
    'Motivated and focused',
    'Romantic and dreamy',
    'Nostalgic',
    'Angry and intense',
    'Peaceful and calm'
  ];

  return (
    <div className="glass-effect rounded-2xl p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-white text-center mb-8">
        🎵 Mood Music
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="mood" className="block text-white/90 text-lg font-medium mb-3">
            How are you feeling today?
          </label>
          <input
            type="text"
            id="mood"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            placeholder="e.g., happy and energetic, sad and reflective, chill and relaxed..."
            className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent"
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          disabled={!mood.trim() || isLoading}
          className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 disabled:hover:scale-100 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Finding Songs...' : 'Get My Playlist 🎶'}
        </button>
      </form>

      <div className="mt-8">
        <p className="text-white/70 text-sm mb-3">Quick suggestions:</p>
        <div className="flex flex-wrap gap-2">
          {moodSuggestions.map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setMood(suggestion)}
              disabled={isLoading}
              className="px-3 py-1 bg-white/10 hover:bg-white/20 rounded-full text-white/80 text-sm transition-all duration-200 hover:scale-105 disabled:hover:scale-100 disabled:cursor-not-allowed"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MoodInput;