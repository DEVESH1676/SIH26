/**
 * Landing page — KarmaSetu hero, features, and footer.
 * Extracted from the original single-file App.tsx.
 */
import {
  ArrowRight, BarChart3, BookOpen, GraduationCap,
  Menu, Network, Sparkles, Target, UsersRound, X,
} from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`brand ${compact ? 'brand-compact' : ''}`}>
      <span className="brand-mark"><Network size={compact ? 17 : 21} /></span>
      <span>
        <strong>KarmaSetu</strong>
        {!compact && <small>National Capacity Bridge</small>}
      </span>
    </div>
  );
}

function FeatureCard({ number, icon, title, description, label, tone }: {
  number: string; icon: React.ReactNode; title: string; description: string; label: string; tone: string;
}) {
  return (
    <article className={`feature-card ${tone}`}>
      <div className="feature-top">
        <span className="feature-icon">{icon}</span>
        <span className="step-pill">STEP {number}</span>
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="feature-label">{label}<ArrowRight size={15} /></div>
    </article>
  );
}

export { Brand };

export default function Landing() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <>
      <header className="site-header">
        <Brand />
        <nav className={mobileOpen ? 'mobile-visible' : ''}>
          <a className="active" href="#home">Home</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#features">Features</a>
          <a href="#about">About</a>
          <button className="header-login" onClick={() => navigate('/login')}>Login</button>
        </nav>
        <button className="menu-button" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
          {mobileOpen ? <X /> : <Menu />}
        </button>
      </header>

      <main id="home">
        <section className="hero section-container">
          <div className="hero-copy fade-up">
            <div className="eyebrow"><Sparkles size={14} /> AI-POWERED SKILL INTELLIGENCE</div>
            <h1>Bridging Skill Gaps.<br /><span>Building a Future-Ready</span><br />Workforce.</h1>
            <p>KarmaSetu connects institutional competency requirements with personalised learning paths, empowering officials to achieve excellence through data-driven insights.</p>
            <div className="hero-actions">
              <button className="primary-button" onClick={() => navigate('/onboarding')}>
                Get Started <ArrowRight size={17} />
              </button>
              <a className="secondary-button" href="#how-it-works">Explore How It Works</a>
            </div>
          </div>
          <div className="hero-visual fade-up delay-1">
            <div className="visual-grid" />
            <div className="core-chip">
              <Network size={30} />
              <strong>KarmaSetu AI</strong>
              <small>Skill Intelligence</small>
            </div>
            <div className="orbit orbit-one"><BarChart3 /><span>Skill<br />Mapping</span></div>
            <div className="orbit orbit-two"><Target /><span>Gap<br />Analysis</span></div>
            <div className="orbit orbit-three"><BookOpen /><span>Targeted<br />Learning</span></div>
            <div className="orbit orbit-four"><UsersRound /><span>Future<br />Workforce</span></div>
            <div className="beam beam-one" />
            <div className="beam beam-two" />
          </div>
        </section>

        <section className="why-section" id="how-it-works">
          <div className="section-container">
            <div className="section-heading">
              <div className="eyebrow">A SYSTEMATIC APPROACH</div>
              <h2>Why KarmaSetu</h2>
              <p>A systematic approach to professional development.</p>
            </div>
            <div className="feature-grid" id="features">
              <FeatureCard number="01" icon={<BarChart3 />} title="Know Your Skills" description="Accurately map your current competencies against standardized functional roles." label="Competency Mapping" tone="blue" />
              <FeatureCard number="02" icon={<Target />} title="Discover Your Gaps" description="Identify critical areas for improvement through precise, data-driven analysis." label="Gap Analysis" tone="gold" />
              <FeatureCard number="03" icon={<GraduationCap />} title="Learn What Matters" description="Receive targeted course recommendations that directly address identified needs." label="Targeted Growth" tone="teal" />
            </div>
          </div>
        </section>
      </main>

      <footer id="about">
        <div className="section-container footer-inner">
          <div>
            <Brand compact />
            <p>© 2024 KarmaSetu. An AI-powered governance initiative.</p>
          </div>
          <div className="footer-links">
            <a href="#about">iGOT Karmayogi</a>
            <a href="#about">NSSTA/TPAC</a>
            <a href="#about">Privacy Policy</a>
            <a href="#about">Terms of Service</a>
            <a href="#about">Contact Support</a>
          </div>
        </div>
      </footer>
    </>
  );
}
