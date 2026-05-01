import React from 'react';

export function Card({ children, className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div 
      className={`bg-background brutal-border p-6 brutal-shadow ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
