/**
 * Profile onboarding wizard — 4-step flow for creating a learner profile.
 * Extracted from the original App.tsx and wired to the backend API.
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft, ArrowRight, Check, ChevronDown, CircleHelp,
  FileCheck2, GraduationCap, Network, Plus, ShieldCheck, Sparkles, UserRound,
} from 'lucide-react';
import type { OnboardingProfile, ProfileStep, SkillLevel } from '../types';
import { Brand } from './Landing';
import * as api from '../lib/api';

const steps = ['Professional', 'Education', 'Skills & Preferences', 'Review'];
const expertiseOptions = ['Data Analysis', 'Statistics', 'Leadership', 'Communication', 'Digital Skills', 'Project Management'];
const focusOptions = ['Data Analysis', 'Leadership', 'Communication', 'Digital Skills'];
const learningFormats = ['Video', 'Reading', 'Practical Exercises', 'Quizzes'];
const learningTimes = ['<2 hours', '2–5 hours', '5–10 hours', '10+ hours'];
const skillNames = ['Data Analysis', 'Communication', 'Leadership', 'Digital Skills'];

function PortalFooter() {
  return (
    <footer className="portal-footer">
      <span><ShieldCheck size={14} /> MeitY & NIC Certified • 256-bit TLS</span>
      <span>Helpdesk &nbsp; • &nbsp; Data Security Policy &nbsp; • &nbsp; © 2024 Digital India / SIH-2024</span>
    </footer>
  );
}

function Progress({ step }: { step: ProfileStep }) {
  return (
    <div className="progress-card">
      {steps.map((label, index) => (
        <div className={`progress-step ${index + 1 <= step ? 'done' : ''} ${index + 1 === step ? 'active' : ''}`} key={label}>
          <div className="progress-node">{index + 1 < step ? <Check size={15} /> : index + 1}</div>
          <strong>{label}</strong>
          <small>{index + 1 < step ? 'COMPLETED' : index + 1 === step ? 'IN PROGRESS' : 'PENDING'}</small>
        </div>
      ))}
    </div>
  );
}

function Field({ label, value, placeholder, onChange }: { label: string; value: string; placeholder?: string; onChange: (v: string) => void }) {
  return (
    <label className="field-label">{label}
      <input value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (v: string) => void }) {
  return (
    <label className="field-label">{label}
      <div className="select-wrap">
        <select value={value} onChange={(e) => onChange(e.target.value)}>
          {options.map((o) => <option key={o}>{o}</option>)}
        </select>
        <ChevronDown size={16} />
      </div>
    </label>
  );
}

function FormHeading({ eyebrow, title, description, icon }: { eyebrow: string; title: string; description: string; icon: React.ReactNode }) {
  return (
    <div className="form-heading">
      <div className="heading-icon">{icon}</div>
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
    </div>
  );
}

function Professional({ profile, updateProfile }: { profile: OnboardingProfile; updateProfile: (k: string, v: any) => void }) {
  return (
    <>
      <FormHeading eyebrow="STEP 1 OF 4: IDENTITY & CADRE" title="Create Your Profile" description="Professional information — establish your cadre identity, departmental assignment, and functional role." icon={<UserRound />} />
      <div className="form-grid">
        <Field label="Full Name" value={profile.name} placeholder="Rahul Sharma" onChange={(v) => updateProfile('name', v)} />
        <Field label="Officer ID / Karmayogi ID" value={profile.officerId} placeholder="CADRE-94821" onChange={(v) => updateProfile('officerId', v)} />
        <SelectField label="Department / Ministry" value={profile.department || 'Ministry of Statistics & Programme Implementation'} options={['Ministry of Statistics & Programme Implementation', 'Ministry of Finance', 'Ministry of Education', 'Ministry of Home Affairs']} onChange={(v) => updateProfile('department', v)} />
        <Field label="Attached Organization / Sub-Cadre" value={profile.organization} placeholder="National Statistical Office / Central Government" onChange={(v) => updateProfile('organization', v)} />
        <SelectField label="Current Designation" value={profile.designation || 'Statistical Officer / Junior Statistical Officer'} options={['Statistical Officer / Junior Statistical Officer', 'Section Officer', 'Deputy Director', 'Assistant Commissioner']} onChange={(v) => updateProfile('designation', v)} />
        <SelectField label="Functional Role" value={profile.role || 'Data Analysis & Survey Sampling'} options={['Data Analysis & Survey Sampling', 'Programme Management', 'Policy & Research', 'Human Resources']} onChange={(v) => updateProfile('role', v)} />
      </div>
      <label className="range-label">
        Years of Public Administration Experience <strong>{profile.years} Years Active</strong>
        <input type="range" min="0" max="35" value={profile.years} onChange={(e) => updateProfile('years', e.target.value)} />
      </label>
      <div className="info-banner">
        <CircleHelp size={17} />
        <span>Information will be used to map role competency against Mission Karmayogi FRAC guidelines and formulate your customized learning trajectory.</span>
      </div>
    </>
  );
}

function Education({ profile, updateProfile, toggleListValue }: {
  profile: OnboardingProfile; updateProfile: (k: string, v: any) => void; toggleListValue: (k: 'expertise' | 'focus', v: string) => void;
}) {
  return (
    <>
      <FormHeading eyebrow="STEP 2 OF 4: QUALIFICATIONS" title="Education & Expertise" description="Document academic qualifications, accreditations, and functional competency domains." icon={<GraduationCap />} />
      <div className="form-grid two">
        <SelectField label="Highest Academic Qualification" value={profile.qualification} options={["Bachelor's Degree", "Master's Degree", 'Doctorate', 'Professional Diploma']} onChange={(v) => updateProfile('qualification', v)} />
        <Field label="Major Field of Study" value={profile.field} placeholder="Statistics" onChange={(v) => updateProfile('field', v)} />
      </div>
      <div className="subsection">
        <div className="subsection-heading">
          <div><h3>Institutional Certifications</h3><p>Government, academy, or accredited technical certifications</p></div>
          <button className="soft-button" onClick={() => updateProfile('certifications', [...profile.certifications, ''])}><Plus size={16} /> Add Certification</button>
        </div>
        {profile.certifications.map((cert, i) => (
          <input className="cert-input" key={i} value={cert} placeholder={i === 0 ? 'e.g. NSSTA Data Analytics Foundation (2023)' : 'Add another certification'} onChange={(e) => updateProfile('certifications', profile.certifications.map((item, j) => j === i ? e.target.value : item))} />
        ))}
      </div>
      <div className="subsection">
        <div className="subsection-heading">
          <div><h3>Areas of Expertise</h3><p>Select all areas that reflect your field deployment experience.</p></div>
          <span className="count-pill">{profile.expertise.length} Selected</span>
        </div>
        <div className="option-grid">
          {expertiseOptions.map((o) => (
            <button className={`select-card ${profile.expertise.includes(o) ? 'selected' : ''}`} key={o} onClick={() => toggleListValue('expertise', o)}>
              <span className="checkbox-mark">{profile.expertise.includes(o) && <Check size={13} />}</span>
              <strong>{o}</strong>
              <small>Competency domain</small>
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

function Skills({ profile, updateProfile, toggleListValue }: {
  profile: OnboardingProfile; updateProfile: (k: string, v: any) => void; toggleListValue: (k: 'expertise' | 'focus', v: string) => void;
}) {
  const setLevel = (name: string, level: SkillLevel) => updateProfile('levels', { ...profile.levels, [name]: level });

  return (
    <>
      <FormHeading eyebrow="STEP 3 OF 4: COMPETENCY CALIBRATION" title="Skills & Learning Preferences" description="Self-rate current competencies and configure your personal learning journey." icon={<Sparkles />} />
      <div className="subsection">
        <h3>Current Skill Level</h3>
        <p className="section-note">Provide an honest baseline for customized capacity-building coursework.</p>
        <div className="skill-list">
          {skillNames.map((name) => (
            <div className="skill-row" key={name}>
              <div><strong>{name}</strong><small>Institutional capability domain</small></div>
              <div className="level-options">
                {(['Beginner', 'Intermediate', 'Advanced'] as SkillLevel[]).map((level) => (
                  <button className={profile.levels[name] === level ? 'selected' : ''} key={level} onClick={() => setLevel(name, level)}>{level}</button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="subsection">
        <h3>What would you like to improve?</h3>
        <p className="section-note">Select targeted skills for accelerated national certification and badge pathways.</p>
        <div className="focus-grid">
          {focusOptions.map((o) => (
            <button className={`focus-card ${profile.focus.includes(o) ? 'selected' : ''}`} key={o} onClick={() => toggleListValue('focus', o)}>
              <span className="focus-check">{profile.focus.includes(o) && <Check size={14} />}</span>
              <strong>{o}</strong>
              <small>Personalized learning pathway</small>
            </button>
          ))}
        </div>
      </div>
      <div className="preference-grid">
        <ChoiceGroup title="Preferred Learning Format" options={learningFormats} selected={profile.format} onSelect={(v) => updateProfile('format', v)} />
        <ChoiceGroup title="Weekly Learning Time" options={learningTimes} selected={profile.time} onSelect={(v) => updateProfile('time', v)} />
      </div>
    </>
  );
}

function ChoiceGroup({ title, options, selected, onSelect }: { title: string; options: string[]; selected: string; onSelect: (v: string) => void }) {
  return (
    <div className="choice-group">
      <h3>{title}</h3>
      {options.map((o) => (
        <button key={o} className={selected === o ? 'selected' : ''} onClick={() => onSelect(o)}>
          <span className="radio-mark" />{o}
        </button>
      ))}
    </div>
  );
}

function ReviewSection({ title, rows }: { title: string; rows: string[][] }) {
  return (
    <section className="review-section">
      <h3>{title}</h3>
      {rows.map(([label, value]) => (
        <div className="review-row" key={label}><span>{label}</span><strong>{value}</strong></div>
      ))}
    </section>
  );
}

function Review({ profile, onEdit }: { profile: OnboardingProfile; onEdit: () => void }) {
  const name = profile.name || 'Rahul Sharma';
  return (
    <>
      <FormHeading eyebrow="STEP 4 OF 4: FINAL REVIEW" title="Review Your Profile" description="Please verify your information before beginning your personalized assessment." icon={<FileCheck2 />} />
      <div className="review-grid">
        <ReviewSection title="Professional" rows={[['Name', name], ['Department', profile.department || 'Ministry of Statistics & Programme Implementation'], ['Designation', profile.designation || 'Officer'], ['Functional Role', profile.role || 'Data Analysis'], ['Experience', `${profile.years} Years`]]} />
        <ReviewSection title="Education" rows={[['Qualification', profile.qualification], ['Field', profile.field || 'Statistics'], ['Certifications', profile.certifications.filter(Boolean).join(', ') || 'Not added']]} />
        <ReviewSection title="Expertise" rows={[['Selected areas', profile.expertise.join(' • ') || 'None selected']]} />
        <ReviewSection title="Learning" rows={[['Preferred format', profile.format], ['Weekly time', profile.time], ['Focus areas', profile.focus.join(' • ') || 'None selected']]} />
      </div>
      <div className="review-note">
        <ShieldCheck size={17} />
        <span>Your profile is securely stored under national civil service guidelines and will be used to personalize your assessment.</span>
      </div>
      <button className="edit-profile" onClick={onEdit}>Edit Profile</button>
    </>
  );
}

export default function ProfileFlow() {
  const navigate = useNavigate();
  const [step, setStep] = useState<ProfileStep>(1);
  const [submitting, setSubmitting] = useState(false);
  const [profile, setProfile] = useState<OnboardingProfile>({
    name: '', officerId: '', department: '', organization: '', designation: '', role: '', years: '3',
    qualification: "Bachelor's Degree", field: '', certifications: [''], expertise: ['Data Analysis', 'Statistics'],
    levels: { 'Data Analysis': 'Intermediate', Communication: 'Intermediate', Leadership: 'Beginner', 'Digital Skills': 'Intermediate' },
    focus: ['Data Analysis', 'Leadership'], format: 'Video', time: '2–5 hours',
  });

  const updateProfile = (key: string, value: any) => setProfile((p) => ({ ...p, [key]: value }));
  const toggleListValue = (key: 'expertise' | 'focus', value: string) =>
    setProfile((p) => ({ ...p, [key]: p[key].includes(value) ? p[key].filter((i) => i !== value) : [...p[key], value] }));

  const nextStep = () => setStep((s) => Math.min(4, s + 1) as ProfileStep);
  const prevStep = () => setStep((s) => Math.max(1, s - 1) as ProfileStep);

  const handleStartAssessment = async () => {
    setSubmitting(true);
    try {
      // Build profile text from collected data
      const profileText = [
        `Name: ${profile.name || 'Not specified'}`,
        `Department: ${profile.department || 'MoSPI'}`,
        `Organization: ${profile.organization}`,
        `Designation: ${profile.designation}`,
        `Role: ${profile.role}`,
        `Experience: ${profile.years} years`,
        `Qualification: ${profile.qualification} in ${profile.field}`,
        `Certifications: ${profile.certifications.filter(Boolean).join(', ')}`,
        `Expertise: ${profile.expertise.join(', ')}`,
        `Skill Levels: ${Object.entries(profile.levels).map(([k, v]) => `${k}: ${v}`).join(', ')}`,
        `Focus Areas: ${profile.focus.join(', ')}`,
        `Learning Format: ${profile.format}`,
        `Weekly Time: ${profile.time}`,
      ].join('\n');

      const designation = profile.designation || 'Statistical Officer';

      // Call the backend competency analysis
      await api.analyzeProfile({
        designation,
        profile_text: profileText,
        department: profile.department || 'Ministry of Statistics & Programme Implementation',
        education: `${profile.qualification} in ${profile.field || 'Statistics'}`,
        experience_years: parseInt(profile.years, 10) || 3,
        previous_trainings: profile.certifications.filter(Boolean),
      });
      toast.success('Profile analysis complete! Redirecting to dashboard...');
      setTimeout(() => navigate('/dashboard'), 1200);
    } catch (err: any) {
      // Even if API fails, let them proceed to dashboard
      toast.error(err.message || 'Analysis unavailable — proceeding to dashboard');
      setTimeout(() => navigate('/dashboard'), 1500);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="profile-page">
      <header className="profile-header">
        <Brand />
        <div className="profile-nav">
          <span className={step >= 1 ? 'current' : ''}>Identity Verification</span>
          <span className={step >= 2 ? 'current' : ''}>Cadre Allocation</span>
          <span className={step >= 3 ? 'current' : ''}>Competency Grid</span>
          <span className={step >= 4 ? 'current' : ''}>Review & Submit</span>
        </div>
        <button className="save-exit" onClick={() => navigate('/')}>Save & Exit</button>
        <span className="avatar"><UserRound size={16} /></span>
      </header>

      <div className="profile-main section-container">
        <div className="flow-meta">
          <span className="eyebrow">FRAC V4.2 ALIGNED</span>
          <span>•</span><span>Onboarding Workflow</span><span>/</span>
          <strong>{steps[step - 1]}</strong>
        </div>

        <Progress step={step} />

        <div className="profile-card">
          {step === 1 && <Professional profile={profile} updateProfile={updateProfile} />}
          {step === 2 && <Education profile={profile} updateProfile={updateProfile} toggleListValue={toggleListValue} />}
          {step === 3 && <Skills profile={profile} updateProfile={updateProfile} toggleListValue={toggleListValue} />}
          {step === 4 && <Review profile={profile} onEdit={prevStep} />}

          <div className="form-actions">
            {step > 1 ? <button className="back-button" onClick={prevStep}><ArrowLeft size={16} /> Back</button> : <span />}
            {step < 4 ? (
              <button className="primary-button" onClick={nextStep}>Continue <ArrowRight size={17} /></button>
            ) : (
              <button className="primary-button" onClick={handleStartAssessment} disabled={submitting}>
                {submitting ? 'Analyzing...' : 'Start Assessment'} <ArrowRight size={17} />
              </button>
            )}
          </div>
        </div>
      </div>

      <PortalFooter />
    </div>
  );
}
