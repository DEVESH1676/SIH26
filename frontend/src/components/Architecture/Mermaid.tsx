import React, { useMemo } from 'react';
import { renderMermaidSVG } from 'beautiful-mermaid';
import { cn } from '../../lib/utils';

interface MermaidCanvasProps {
  chart: string;
  className?: string;
  id?: string;
}

const MermaidCanvas: React.FC<MermaidCanvasProps> = ({ chart, className, id }) => {
  const svgContent = useMemo(() => {
    try {
      return renderMermaidSVG(chart, {
        bg: 'transparent',
        fg: '#f8fafc',
        line: '#64748b',
        accent: '#22d3ee',
        surface: 'rgba(34,211,238,0.1)',
        border: '#22d3ee',
        transparent: true
      });
    } catch (e) {
      console.error(e);
      return '<p>Error rendering diagram</p>';
    }
  }, [chart]);

  return (
    <div 
      id={id} 
      className={cn('glass border border-white/10 rounded-2xl p-8', className)}
      dangerouslySetInnerHTML={{ __html: svgContent }}
    />
  );
};

export default MermaidCanvas;
