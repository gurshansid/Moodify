import React from 'react';
import type { RecommendationResponse } from '../types';
import TrackCard from './TrackCard';

interface TrackListProps {
  data: RecommendationResponse;
  onNewSearch: () => void;
}

const TrackList: React.FC<TrackListProps> = ({ data, onNewSearch }) => {
  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="glass-effect rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">
              Perfect for "{data.mood}"
            </h2>
            <p className="text-white/80">
              Found {data.total_found} songs that match your vibe
            </p>
          </div>
          <button
            onClick={onNewSearch}
            className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-all duration-200"
          >
            New Search
          </button>
        </div>
      </div>

      {/* Track List */}
      <div className="space-y-4">
        {data.tracks.map((track, index) => (
          <TrackCard key={`${track.name}-${track.artist}-${index}`} track={track} />
        ))}
      </div>

      {/* Footer */}
      <div className="text-center mt-8">
        <button
          onClick={onNewSearch}
          className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-200 transform hover:scale-105"
        >
          Discover More Music 🎵
        </button>
      </div>
    </div>
  );
};

export default TrackList;