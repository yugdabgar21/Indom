"use client";

import React, { useState } from 'react';
import Image from 'next/image';
import SettingsModal from './SettingsModal';

export default function HeaderClient() {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <>
      <header className="mb-12 flex justify-between items-center brutal-border p-4 bg-background brutal-shadow-sm">
        <div className="flex items-center gap-3">
          <h1 className="text-3xl tracking-tighter text-accent font-heading">INDOM<span className="text-foreground">.</span></h1>
        </div>
        <div className="flex items-center gap-4">
          <p className="text-xs uppercase hidden md:block font-sans font-bold">Your CV. Their requirements. No mercy.</p>
          <button
            onClick={() => setShowSettings(true)}
            className="text-[#888] hover:text-accent transition-colors p-2"
            title="Settings"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
            </svg>
          </button>
        </div>
      </header>
      <SettingsModal isOpen={showSettings} onClose={() => setShowSettings(false)} />
    </>
  );
}
