import React, { useState, useRef } from 'react';
import type { Track } from '../types';

interface TrackCardProps {
  track: Track;
}

const TrackCard: React.FC<TrackCardProps> = ({ track }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const formatDuration = (ms: number) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const handlePlayPreview = async () => {
    if (!track.preview_url) return;

    try {
      if (!audioRef.current) {
        audioRef.current = new Audio(track.preview_url);
        audioRef.current.volume = 0.7;
      }

      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        setIsLoading(true);
        await audioRef.current.play();
        setIsPlaying(true);
        setIsLoading(false);

        // Auto-pause after 30 seconds
        audioRef.current.onended = () => {
          setIsPlaying(false);
        };
      }
    } catch (error) {
      console.error('Error playing audio:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-effect rounded-xl p-4 hover:bg-white/30 transition-all duration-300 transform hover:scale-[1.02]">
      <div className="flex items-center space-x-4">
        {/* Album Art */}
        <div className="relative flex-shrink-0">
          <img
            src={track.image_url || 'https://via.placeholder.com/80x80?text=♪'}
            alt={`${track.album} cover`}
            className="w-16 h-16 rounded-lg object-cover"
          />
          
          {/* Play/Pause Button Overlay */}
          {track.preview_url && (
            <button
              onClick={handlePlayPreview}
              disabled={isLoading}
              className="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-200"
            >
              {isLoading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin">
                </div>
              ) : (
                <div className="text-white text-xl">
                  {isPlaying ? '⏸️' : '▶️'}
                </div>
              )}
            </button>
          )}
        </div>

        {/* Track Info */}
        <div className="flex-grow min-w-0">
          <h3 className="font-semibold text-white text-lg truncate">
            {track.name}
          </h3>
          <p className="text-white/80 truncate">
            {track.artist}
          </p>
          <p className="text-white/60 text-sm truncate">
            {track.album}
          </p>

          {/* Metadata */}
          <div className="flex items-center space-x-3 mt-1">
            {track.popularity && (
              <span className="text-white/50 text-xs">
                ⭐ {track.popularity}%
              </span>
            )}
            {track.duration_ms && (
              <span className="text-white/50 text-xs">
                🕒 {formatDuration(track.duration_ms)}
              </span>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex flex-col space-y-2">
          <a
            href={track.spotify_url}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-lg text-sm font-medium transition-colors duration-200"
          >
            Open in Spotify
          </a>
          {!track.preview_url && (
            <span className="text-white/40 text-xs text-center">
              No preview available
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default TrackCard;