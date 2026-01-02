const { useState } = React;

function App() {
    const [origin, setOrigin] = useState("casablanca");
    const [destination, setDestination] = useState("");
    const [budget, setBudget] = useState(15000);  // Default ~1500 EUR in MAD
    const [numPeople, setNumPeople] = useState(2);
    const [duration, setDuration] = useState(5);

    // Priority sliders
    const [ecoPriority, setEcoPriority] = useState(60);
    const [budgetPriority, setBudgetPriority] = useState(25);
    const [durationPriority, setDurationPriority] = useState(15);

    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [selectedTrip, setSelectedTrip] = useState(null);
    const [showForm, setShowForm] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResults([]);
        setSelectedTrip(null);

        try {
            const response = await fetch('http://127.0.0.1:8015/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    origin: origin,
                    destination_filter: destination || null,
                    max_budget: parseFloat(budget),
                    num_people: parseInt(numPeople),
                    duration_days: parseInt(duration),
                    eco_priority: parseInt(ecoPriority),
                    budget_priority: parseInt(budgetPriority),
                    duration_priority: parseInt(durationPriority)
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const budgetPercent = ((budget - 2000) / (20000 - 2000)) * 100;

    // Transport icon helper
    const getTransportIcon = (transport) => {
        if (transport.includes('train')) {
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
            );
        } else if (transport.includes('bus')) {
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002-2v-2" />
                </svg>
            );
        } else {
            return (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
            );
        }
    };

    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            {!showForm && (
                <div className="container mx-auto px-4 py-16 fade-in">
                    <div className="max-w-4xl mx-auto text-center">
                        <div className="mb-6">
                            <span className="badge">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                                Voyagez responsable
                            </span>
                        </div>

                        <h1 className="hero-title mb-6">
                            Voyagez mieux,<br />
                            <span style={{ color: '#1e293b' }}>pas plus loin</span>
                        </h1>

                        <p className="hero-subtitle max-w-2xl mx-auto mb-10">
                            Découvrez des destinations qui respectent votre budget,<br />
                            votre temps <span style={{ color: '#047857', fontWeight: 600 }}>et la planète</span>.
                        </p>

                        <div className="flex gap-4 justify-center mb-16">
                            <button onClick={() => setShowForm(true)} className="btn-primary">
                                Planifier mon voyage
                            </button>
                            <button className="btn-secondary">
                                Comment ça marche ?
                            </button>
                        </div>

                        {/* Feature Cards */}
                        <div className="grid md:grid-cols-3 gap-6 mt-12">
                            <div className="card text-left">
                                <div className="w-12 h-12 bg-[#ecfdf5] rounded-full flex items-center justify-center mb-4">
                                    <svg className="w-6 h-6 text-[#17E89C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-lg mb-2">CO₂ optimisé</h3>
                                <p className="text-gray-600 text-sm">Empreinte minimale pour chaque trajet</p>
                            </div>

                            <div className="card text-left">
                                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-lg mb-2">Multi-critères</h3>
                                <p className="text-gray-600 text-sm">Budget, durée, impact environnemental</p>
                            </div>

                            <div className="card text-left">
                                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-lg mb-2">Explications</h3>
                                <p className="text-gray-600 text-sm">Comprenez chaque recommandation</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Form Section */}
            {showForm && (
                <div className="container mx-auto px-4 py-12 fade-in">
                    <div className="max-w-6xl mx-auto">
                        <button
                            onClick={() => setShowForm(false)}
                            className="mb-6 text-gray-600 hover:text-gray-900 flex items-center gap-2"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                            Retour
                        </button>

                        <div className="text-center mb-12">
                            <h2 className="section-title">Définissez votre voyage idéal</h2>
                            <p className="section-subtitle">
                                Nous analyserons des milliers d'options pour trouver le meilleur équilibre entre<br />
                                vos critères et l'impact environnemental.
                            </p>
                        </div>

                        <div className="grid lg:grid-cols-2 gap-8">
                            {/* Form Card */}
                            <div>
                                <form onSubmit={handleSearch} className="card space-y-8">
                                    {/* Itinerary Section */}
                                    <div>
                                        <div className="flex items-center gap-2 mb-4">
                                            <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            <h3 className="font-semibold text-lg">Itinéraire et dates</h3>
                                        </div>
                                        <p className="text-sm text-gray-600 mb-4">D'où partez-vous et où souhaitez-vous aller ?</p>

                                        <div className="grid md:grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-sm font-medium text-gray-700 mb-2">Ville de départ</label>
                                                <select
                                                    value={origin}
                                                    onChange={(e) => setOrigin(e.target.value)}
                                                    className="input-field"
                                                >
                                                    <option value="casablanca">Casablanca</option>
                                                    <option value="rabat">Rabat</option>
                                                    <option value="marrakech">Marrakech</option>
                                                    <option value="fes">Fès</option>
                                                    <option value="tanger">Tanger</option>
                                                    <option value="agadir">Agadir</option>
                                                    <option value="meknes">Meknès</option>
                                                    <option value="ouarzazate">Ouarzazate</option>
                                                    <option value="essaouira">Essaouira</option>
                                                    <option value="chefchaouen">Chefchaouen</option>
                                                </select>
                                            </div>

                                            <div>
                                                <label className="block text-sm font-medium text-gray-700 mb-2">Destination (Recommandé)</label>
                                                <select
                                                    value={destination}
                                                    onChange={(e) => setDestination(e.target.value)}
                                                    className="input-field"
                                                >
                                                    <option value="">Laissez-nous vous inspirer (Toutes)</option>
                                                    <option value="marrakech">Marrakech</option>
                                                    <option value="chefchaouen">Chefchaouen</option>
                                                    <option value="essaouira">Essaouira</option>
                                                    <option value="fes">Fès</option>
                                                    <option value="casablanca">Casablanca</option>
                                                    <option value="ouarzazate">Ouarzazate</option>
                                                    <option value="tanger">Tanger</option>
                                                    <option value="agadir">Agadir</option>
                                                    <option value="meknes">Meknès</option>
                                                </select>
                                            </div>

                                            <div>
                                                <label className="block text-sm font-medium text-gray-700 mb-2">Durée du séjour</label>
                                                <input
                                                    type="number"
                                                    value={duration}
                                                    onChange={(e) => setDuration(e.target.value)}
                                                    className="input-field"
                                                    min="1"
                                                    max="30"
                                                />
                                                <p className="text-xs text-gray-500 mt-1">{duration} jour{duration > 1 ? 's' : ''}</p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Budget Section */}
                                    <div>
                                        <div className="flex items-center gap-2 mb-4">
                                            <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                                            </svg>
                                            <h3 className="font-semibold text-lg">Budget et voyageurs</h3>
                                        </div>

                                        <div className="space-y-6">
                                            <div>
                                                <div className="flex justify-between items-center mb-3">
                                                    <label className="text-sm font-medium text-gray-700">Budget total</label>
                                                    <span className="text-2xl font-bold" style={{ color: '#047857' }}>{budget} DH</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="2000"
                                                    max="20000"
                                                    step="500"
                                                    value={budget}
                                                    onChange={(e) => setBudget(e.target.value)}
                                                    style={{ '--value': `${budgetPercent}%` }}
                                                />
                                                <div className="flex justify-between text-xs text-gray-500 mt-1">
                                                    <span>2 000 DH</span>
                                                    <span>20 000 DH</span>
                                                </div>
                                            </div>

                                            <div>
                                                <div className="flex justify-between items-center mb-3">
                                                    <label className="text-sm font-medium text-gray-700">Nombre de voyageurs</label>
                                                    <div className="flex items-center gap-3">
                                                        <button
                                                            type="button"
                                                            onClick={() => setNumPeople(Math.max(1, numPeople - 1))}
                                                            className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-[#17E89C] hover:text-[#17E89C] transition"
                                                        >
                                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
                                                            </svg>
                                                        </button>
                                                        <span className="text-2xl font-bold w-12 text-center">{numPeople}</span>
                                                        <button
                                                            type="button"
                                                            onClick={() => setNumPeople(Math.min(10, numPeople + 1))}
                                                            className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-[#17E89C] hover:text-[#17E89C] transition"
                                                        >
                                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                                            </svg>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Priorities Section */}
                                    <div>
                                        <div className="flex items-center gap-2 mb-4">
                                            <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                                            </svg>
                                            <h3 className="font-semibold text-lg">Vos priorités</h3>
                                        </div>
                                        <p className="text-sm text-gray-600 mb-4">Ajustez l'importance de chaque critère dans nos recommandations</p>

                                        <div className="space-y-5">
                                            <div>
                                                <div className="flex justify-between items-center mb-2">
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-3 h-3 rounded-full bg-[#17E89C]"></div>
                                                        <label className="text-sm font-medium text-gray-700">Impact écologique</label>
                                                    </div>
                                                    <span className="text-lg font-bold text-[#047857]">{ecoPriority}%</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="0"
                                                    max="100"
                                                    value={ecoPriority}
                                                    onChange={(e) => setEcoPriority(parseInt(e.target.value))}
                                                    style={{ '--value': `${ecoPriority}%` }}
                                                />
                                            </div>

                                            <div>
                                                <div className="flex justify-between items-center mb-2">
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                                                        <label className="text-sm font-medium text-gray-700">Économies budgétaires</label>
                                                    </div>
                                                    <span className="text-lg font-bold text-orange-600">{budgetPriority}%</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="0"
                                                    max="100"
                                                    value={budgetPriority}
                                                    onChange={(e) => setBudgetPriority(parseInt(e.target.value))}
                                                    style={{ '--value': `${budgetPriority}%` }}
                                                />
                                            </div>

                                            <div>
                                                <div className="flex justify-between items-center mb-2">
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                                                        <label className="text-sm font-medium text-gray-700">Durée du trajet</label>
                                                    </div>
                                                    <span className="text-lg font-bold text-blue-600">{durationPriority}%</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="0"
                                                    max="100"
                                                    value={durationPriority}
                                                    onChange={(e) => setDurationPriority(parseInt(e.target.value))}
                                                    style={{ '--value': `${durationPriority}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        disabled={loading}
                                        className="btn-primary w-full flex items-center justify-center gap-2"
                                    >
                                        {loading ? 'Recherche en cours...' : 'Trouver mes options'}
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                        </svg>
                                    </button>
                                </form>
                            </div>

                            {/* Results Section */}
                            <div>
                                <div className="card sticky top-4">
                                    <h3 className="font-semibold text-lg mb-4">Recommandations</h3>

                                    {error && (
                                        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                                            <p className="text-red-700 text-sm">{error}</p>
                                        </div>
                                    )}

                                    {results.length === 0 && !loading && !error && (
                                        <div className="text-center py-8">
                                            <svg className="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                                            </svg>
                                            <p className="text-gray-500 text-sm">Aucune recommandation pour le moment.<br />Ajustez vos critères et lancez la recherche !</p>
                                        </div>
                                    )}

                                    {results.length > 0 && (
                                        <div className="space-y-4">
                                            {results.map((trip, idx) => {
                                                const isBest = idx === 0;
                                                // Handle parsing of explanation if needed, or just use structured data
                                                const transportType = trip.transport.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

                                                // Format Duration
                                                const hours = Math.floor(trip.duration);
                                                const minutes = Math.round((trip.duration - hours) * 60);
                                                const timeString = `${hours}h${minutes > 0 ? minutes : ''}`;

                                                return (
                                                    <div
                                                        key={idx}
                                                        onClick={() => setSelectedTrip(selectedTrip === trip ? null : trip)}
                                                        className={`bg-white rounded-2xl p-6 mb-4 cursor-pointer border-[4px] transition-all duration-300 ${isBest
                                                            ? 'border-[#17E89C] shadow-lg ring-2 ring-[#17E89C]/20'
                                                            : 'border-gray-400 shadow-md hover:border-[#17E89C] hover:shadow-lg'
                                                            }`}
                                                    >
                                                        {/* Top Badge */}
                                                        {isBest && (
                                                            <div className="flex items-center gap-2 text-[#047857] font-semibold text-sm mb-4">
                                                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                                </svg>
                                                                Top Recommandation
                                                            </div>
                                                        )}

                                                        {/* Main Content */}
                                                        <div className="flex items-start justify-between mb-5">
                                                            <div className="flex gap-4 flex-1">
                                                                <div className="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center text-3xl flex-shrink-0">
                                                                    {getTransportIcon(trip.transport)}
                                                                </div>
                                                                <div className="flex-1">
                                                                    <h3 className="font-bold text-xl text-gray-900 mb-1">{transportType}</h3>
                                                                    <div className="text-gray-500 text-base flex items-center gap-4 flex-wrap">
                                                                        <span className="flex items-center gap-1.5">
                                                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                                            </svg>
                                                                            {timeString}
                                                                        </span>
                                                                        <span>•</span>
                                                                        <span className="capitalize">{origin} → {trip.destination}</span>
                                                                    </div>
                                                                </div>
                                                            </div>

                                                            <div className="text-right ml-4">
                                                                <div className="text-[#047857] text-3xl font-bold mb-1">{Math.round(trip.cost)} DH</div>
                                                                <div className="text-gray-400 text-sm mb-2">pour {numPeople} pers.</div>
                                                                <div className="text-sm font-semibold text-gray-700">{Math.round(trip.co2)} kg <span className="text-gray-400 font-normal">CO₂</span></div>
                                                            </div>
                                                        </div>

                                                        {/* Score Bar */}
                                                        <div className="mb-4">
                                                            <div className="flex justify-between text-sm mb-2 text-gray-600">
                                                                <span className="font-medium">Score global</span>
                                                                <span className="font-bold text-[#047857]">{Math.round(trip.score)}/100</span>
                                                            </div>
                                                            <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                                                                <div
                                                                    className="h-full rounded-full transition-all duration-500"
                                                                    style={{
                                                                        width: `${Math.min(100, Math.max(0, trip.score))}%`,
                                                                        backgroundColor: trip.score > 80 ? '#17E89C' : trip.score > 50 ? '#fbbf24' : '#ef4444'
                                                                    }}
                                                                ></div>
                                                            </div>
                                                        </div>

                                                        {/* Expanded Details */}
                                                        {selectedTrip === trip && (
                                                            <div className="mt-6 pt-6 border-t border-gray-200 animate-fadeIn">
                                                                <div className="grid md:grid-cols-2 gap-6">
                                                                    {/* Pros & Cons */}
                                                                    <div className="bg-gray-50 rounded-xl p-5">
                                                                        <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-gray-800">
                                                                            <svg className="w-5 h-5 text-[#17E89C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                                            </svg>
                                                                            Avantages & Inconvénients
                                                                        </h4>
                                                                        <ul className="text-sm text-gray-600 space-y-2 list-none">
                                                                            {trip.transport.toLowerCase().includes('train') && (
                                                                                <>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Confort supérieur</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Centre-ville à centre-ville</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Faible empreinte carbone</span>
                                                                                    </li>
                                                                                </>
                                                                            )}
                                                                            {trip.transport.toLowerCase().includes('bus') && (
                                                                                <>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Option la plus économique</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Réseau étendu</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-orange-500 font-bold">⚠</span>
                                                                                        <span className="text-orange-600">Trajet plus long</span>
                                                                                    </li>
                                                                                </>
                                                                            )}
                                                                            {trip.transport.toLowerCase().includes('car') && (
                                                                                <>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Liberté totale</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Idéal pour les groupes</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-orange-500 font-bold">⚠</span>
                                                                                        <span className="text-orange-600">Conduite et stationnement</span>
                                                                                    </li>
                                                                                </>
                                                                            )}
                                                                            {trip.transport.toLowerCase().includes('taxi') && (
                                                                                <>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Rapide et direct</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-[#047857] font-bold">✓</span>
                                                                                        <span className="text-[#047857] font-medium">Porte à porte</span>
                                                                                    </li>
                                                                                    <li className="flex items-start gap-2">
                                                                                        <span className="text-orange-500 font-bold">⚠</span>
                                                                                        <span className="text-orange-600">Espace limité</span>
                                                                                    </li>
                                                                                </>
                                                                            )}
                                                                        </ul>
                                                                    </div>

                                                                    {/* Details */}
                                                                    <div className="bg-white border-2 border-gray-100 rounded-xl p-5">
                                                                        <h4 className="font-bold text-base mb-3 text-gray-800">Détails du voyage</h4>
                                                                        <p className="text-sm text-gray-600 leading-relaxed">
                                                                            {trip.explanation}
                                                                        </p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    )
                                    }
                                </div >
                            </div >
                        </div >
                    </div >
                </div >
            )
            }
        </div >
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);