
import React, { useState, useEffect, useMemo } from 'react';
import { View, MenuItem, CartItem, Order } from './types';
import { INITIAL_MENU, WHATSAPP_NUMBER, CALL_NUMBER, ADMIN_PASS } from './constants';
import { getChefRecommendation } from './services/geminiService';

// --- Icon Components (SVG) to avoid SyntaxErrors with raw emojis ---
const Icons = {
  Home: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>,
  Menu: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" /></svg>,
  Reserve: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" /></svg>,
  Cart: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" /></svg>,
  Admin: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 0 1 1.45.12l.773.774a1.125 1.125 0 0 1 .12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738a1.125 1.125 0 0 1-.12 1.45l-.772.773a1.125 1.125 0 0 1-1.45.12l-.737-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527a1.125 1.125 0 0 1-1.45-.12l-.773-.774a1.125 1.125 0 0 1-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.108-1.204l-.526-.738a1.125 1.125 0 0 1 .12-1.45l.773-.773a1.125 1.125 0 0 1 1.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894Z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0" /></svg>,
  Call: () => <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.387a12.035 12.035 0 0 1-7.143-7.143c-.155-.441.011-.928.387-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" /></svg>
};

// --- Helper Components ---

const Navbar: React.FC<{ 
  currentView: View, 
  setView: (v: View) => void, 
  cartCount: number 
}> = ({ currentView, setView, cartCount }) => (
  <nav className="fixed bottom-0 left-0 right-0 z-50 bg-zinc-900/90 border-t border-amber-500/20 md:top-0 md:bottom-auto md:border-b md:border-t-0 p-2 md:px-8 flex justify-around md:justify-between items-center backdrop-blur-xl transition-all">
    <div className="hidden md:flex items-center gap-2">
      <div className="w-8 h-8 bg-amber-500 rounded-lg flex items-center justify-center text-black font-bold">T</div>
      <h1 className="text-xl text-amber-500 font-bold tracking-widest uppercase font-serif">Teranga Express</h1>
    </div>
    <div className="flex gap-2 md:gap-8 overflow-x-auto no-scrollbar">
      <NavItem active={currentView === 'home'} onClick={() => setView('home')} icon={<Icons.Home />} label="Accueil" />
      <NavItem active={currentView === 'menu'} onClick={() => setView('menu')} icon={<Icons.Menu />} label="La Carte" />
      <NavItem active={currentView === 'reserve'} onClick={() => setView('reserve')} icon={<Icons.Reserve />} label="Réserver" />
      <NavItem active={currentView === 'cart'} onClick={() => setView('cart')} icon={<Icons.Cart />} label={`Panier`} badge={cartCount > 0 ? cartCount : undefined} />
      <NavItem active={currentView === 'admin'} onClick={() => setView('admin')} icon={<Icons.Admin />} label="Admin" />
    </div>
    <div className="hidden md:block">
      <a href={`tel:${CALL_NUMBER}`} className="flex items-center gap-2 px-5 py-2.5 bg-zinc-800 border border-amber-500/30 text-amber-500 rounded-full hover:bg-amber-500 hover:text-black transition-all font-bold shadow-lg shadow-amber-500/10">
        <Icons.Call /> {CALL_NUMBER}
      </a>
    </div>
  </nav>
);

const NavItem: React.FC<{ active: boolean, onClick: () => void, icon: React.ReactNode, label: string, badge?: number }> = ({ active, onClick, icon, label, badge }) => (
  <button 
    onClick={onClick}
    className={`relative flex flex-col items-center justify-center p-2 min-w-[70px] transition-all rounded-xl ${active ? 'text-amber-500 bg-amber-500/10' : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'}`}
  >
    <div className={`${active ? 'scale-110' : ''} transition-transform`}>{icon}</div>
    <span className="text-[9px] uppercase font-bold tracking-wider mt-1">{label}</span>
    {badge !== undefined && (
      <span className="absolute top-1 right-2 bg-amber-500 text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center animate-bounce">
        {badge}
      </span>
    )}
  </button>
);

// --- Main App ---

const App: React.FC = () => {
  const [view, setView] = useState<View>('home');
  const [menu, setMenu] = useState<MenuItem[]>(() => {
    const saved = localStorage.getItem('tg_menu');
    return saved ? JSON.parse(saved) : INITIAL_MENU;
  });
  const [cart, setCart] = useState<CartItem[]>([]);
  const [orders, setOrders] = useState<Order[]>(() => {
    const saved = localStorage.getItem('tg_orders');
    return saved ? JSON.parse(saved) : [];
  });
  const [aiMessage, setAiMessage] = useState("Bonjour ! Je suis le Chef. Besoin d'un conseil pour votre commande ?");
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [adminCode, setAdminCode] = useState("");

  useEffect(() => {
    localStorage.setItem('tg_menu', JSON.stringify(menu));
  }, [menu]);

  useEffect(() => {
    localStorage.setItem('tg_orders', JSON.stringify(orders));
  }, [orders]);

  const addToCart = (item: MenuItem) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) {
        return prev.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      }
      return [...prev, { ...item, quantity: 1 }];
    });
  };

  const removeFromCart = (id: string) => {
    setCart(prev => prev.filter(i => i.id !== id));
  };

  const updateQuantity = (id: string, delta: number) => {
    setCart(prev => prev.map(item => {
      if (item.id === id) {
        const newQty = Math.max(1, item.quantity + delta);
        return { ...item, quantity: newQty };
      }
      return item;
    }));
  };

  const cartCount = useMemo(() => cart.reduce((acc, curr) => acc + curr.quantity, 0), [cart]);
  const cartTotal = useMemo(() => cart.reduce((acc, curr) => acc + (curr.price * curr.quantity), 0), [cart]);

  const handleAskChef = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const input = (e.currentTarget.elements.namedItem('aiPrompt') as HTMLInputElement).value;
    if (!input) return;
    
    setIsAiLoading(true);
    const reply = await getChefRecommendation(input, menu);
    setAiMessage(reply);
    setIsAiLoading(false);
    e.currentTarget.reset();
  };

  const handleCheckout = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const type = formData.get('type') as any;
    const logistics = formData.get('logistics') as string;

    if (!logistics) return alert("Veuillez préciser la table ou l'adresse.");

    const newOrder: Order = {
      id: Math.random().toString(36).substr(2, 9),
      items: [...cart],
      total: cartTotal,
      type,
      logistics,
      timestamp: Date.now(),
    };

    setOrders([newOrder, ...orders]);
    
    const itemString = cart.map(i => `- ${i.name} (x${i.quantity})`).join('\n');
    const msg = `🥘 *NOUVELLE COMMANDE*\n\n${itemString}\n\n💰 Total: ${cartTotal} FCFA\n📍 Mode: ${type}\n📝 Détails: ${logistics}`;
    const waLink = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;
    
    window.open(waLink, '_blank');
    setCart([]);
    setView('home');
  };

  return (
    <div className="min-h-screen pb-24 md:pt-24 bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-amber-500/30">
      <Navbar currentView={view} setView={setView} cartCount={cartCount} />

      <main className="flex-1 container mx-auto px-4 max-w-6xl py-4">
        
        {/* VIEW: HOME */}
        {view === 'home' && (
          <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="relative rounded-[2.5rem] overflow-hidden h-[450px] flex items-center justify-center shadow-2xl group">
              <img 
                src="https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp" 
                className="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:scale-105 transition-transform duration-1000"
                alt="Banner"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-transparent to-transparent"></div>
              <div className="relative z-10 text-center space-y-6 px-4">
                <div className="inline-block px-4 py-1.5 bg-amber-500/10 border border-amber-500/30 rounded-full text-amber-500 text-xs font-bold uppercase tracking-widest mb-2">Teranga Gourmet Dakar</div>
                <h1 className="text-5xl md:text-8xl font-serif text-amber-500 drop-shadow-lg">Goutez au Terroir</h1>
                <p className="text-xl md:text-3xl font-light italic text-zinc-200 max-w-2xl mx-auto">Une cuisine généreuse, une hospitalité authentique.</p>
                <div className="flex flex-wrap justify-center gap-4 pt-4">
                    <button 
                    onClick={() => setView('menu')}
                    className="px-10 py-4 bg-amber-500 text-black font-extrabold rounded-2xl hover:bg-amber-400 transition-all shadow-xl shadow-amber-500/20 active:scale-95"
                    >
                    Explorer la Carte
                    </button>
                    <a href={`tel:${CALL_NUMBER}`} className="px-10 py-4 bg-zinc-900 border border-zinc-700 text-white font-bold rounded-2xl hover:bg-zinc-800 transition-all flex items-center gap-2">
                      <Icons.Call /> Appeler
                    </a>
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-8 items-stretch">
              <div className="bg-zinc-900/50 backdrop-blur-md p-8 rounded-[2rem] border border-white/5 shadow-xl flex flex-col justify-between">
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center text-black">👨‍🍳</div>
                    <h2 className="text-2xl font-serif text-amber-500">Le Conseil du Chef IA</h2>
                  </div>
                  <div className="bg-zinc-800/80 p-6 rounded-2xl border-l-4 border-amber-500 shadow-inner min-h-[120px] relative overflow-hidden">
                    <p className={`text-zinc-200 leading-relaxed ${isAiLoading ? 'animate-pulse opacity-50' : ''}`}>
                      {isAiLoading ? "Notre Chef consulte ses recettes..." : aiMessage}
                    </p>
                  </div>
                </div>
                <form onSubmit={handleAskChef} className="mt-6 flex gap-2">
                  <input 
                    name="aiPrompt"
                    required
                    placeholder="Qu'est-ce qui est bon pour un dîner léger ?" 
                    className="flex-1 bg-zinc-900 border border-zinc-700 rounded-xl px-5 py-3.5 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all text-sm"
                  />
                  <button type="submit" disabled={isAiLoading} className="bg-amber-500 text-black px-6 rounded-xl font-bold hover:bg-amber-400 disabled:opacity-50 transition-all">
                    Envoyer
                  </button>
                </form>
              </div>
              <div className="relative rounded-[2rem] overflow-hidden min-h-[300px] shadow-2xl">
                <img 
                    src="https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800" 
                    className="w-full h-full object-cover"
                    alt="Chef"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-zinc-950/40 to-transparent"></div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW: MENU */}
        {view === 'menu' && (
          <div className="space-y-10 animate-in slide-in-from-bottom-8 duration-700">
            <div className="text-center space-y-4">
              <h1 className="text-5xl font-serif text-amber-500">La Carte Teranga</h1>
              <p className="text-zinc-400 max-w-xl mx-auto">Découvrez nos spécialités cuisinées avec amour et tradition.</p>
              <div className="flex justify-center gap-2 pt-4">
                {['Tous', 'Plat', 'Entrée', 'Boisson'].map(cat => (
                  <button key={cat} className={`px-4 py-1.5 rounded-full text-xs font-bold transition-all ${cat === 'Tous' ? 'bg-amber-500 text-black' : 'bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white'}`}>
                    {cat}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {menu.map(item => (
                <div key={item.id} className="bg-zinc-900 rounded-[2rem] overflow-hidden border border-zinc-800/50 hover:border-amber-500/30 transition-all group flex flex-col shadow-lg hover:shadow-amber-500/5">
                  <div className="relative h-60 overflow-hidden">
                    <img src={item.image} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" alt={item.name} />
                    <div className="absolute bottom-4 left-4">
                      <div className="bg-black/80 backdrop-blur-md px-4 py-1.5 rounded-full text-amber-500 font-extrabold text-sm border border-amber-500/20">
                        {item.price.toLocaleString()} FCFA
                      </div>
                    </div>
                  </div>
                  <div className="p-6 space-y-4 flex-1 flex flex-col justify-between">
                    <div className="space-y-2">
                      <h3 className="text-2xl font-serif font-bold group-hover:text-amber-500 transition-colors">{item.name}</h3>
                      <p className="text-zinc-400 text-sm leading-relaxed">{item.description}</p>
                    </div>
                    <button 
                      onClick={() => addToCart(item)}
                      className="w-full py-4 bg-zinc-800 border-2 border-transparent hover:border-amber-500/50 text-white hover:text-amber-500 rounded-2xl font-bold transition-all flex items-center justify-center gap-2 active:scale-95"
                    >
                      <Icons.Cart /> Ajouter au Panier
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* VIEW: RESERVE */}
        {view === 'reserve' && (
          <div className="max-w-3xl mx-auto space-y-10 animate-in zoom-in-95 duration-500">
             <div className="relative rounded-[2.5rem] overflow-hidden h-56 shadow-xl">
              <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800" className="w-full h-full object-cover opacity-40" alt="Res" />
              <div className="absolute inset-0 flex flex-col items-center justify-center space-y-2">
                <h1 className="text-5xl font-serif text-amber-500">Privilège Teranga</h1>
                <p className="text-zinc-300">Réservez votre table pour une expérience inoubliable</p>
              </div>
            </div>
            
            <form className="bg-zinc-900/50 backdrop-blur-md p-10 rounded-[2.5rem] border border-white/5 space-y-8 shadow-2xl" onSubmit={(e) => {
              e.preventDefault();
              const d = new FormData(e.currentTarget);
              const msg = `📝 *RÉSERVATION TABLE*\n\n👤 Nom: ${d.get('nom')}\n📅 Date: ${d.get('date')}\n⏰ Heure: ${d.get('heure')}\n👥 Personnes: ${d.get('pers')}`;
              window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
            }}>
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-3">
                  <label className="text-xs uppercase font-bold text-zinc-500 tracking-widest">Votre Nom complet</label>
                  <input name="nom" required className="w-full bg-zinc-800 border-transparent focus:bg-zinc-700 focus:ring-2 focus:ring-amber-500/50 rounded-2xl p-4 transition-all" placeholder="Prénom Nom" />
                </div>
                <div className="space-y-3">
                  <label className="text-xs uppercase font-bold text-zinc-500 tracking-widest">Nombre de Convives</label>
                  <input name="pers" type="number" defaultValue="2" min="1" className="w-full bg-zinc-800 border-transparent focus:bg-zinc-700 focus:ring-2 focus:ring-amber-500/50 rounded-2xl p-4 transition-all" />
                </div>
                <div className="space-y-3">
                  <label className="text-xs uppercase font-bold text-zinc-500 tracking-widest">Date de visite</label>
                  <input name="date" type="date" required className="w-full bg-zinc-800 border-transparent focus:bg-zinc-700 focus:ring-2 focus:ring-amber-500/50 rounded-2xl p-4 transition-all text-white" />
                </div>
                <div className="space-y-3">
                  <label className="text-xs uppercase font-bold text-zinc-500 tracking-widest">Heure</label>
                  <input name="heure" type="time" required className="w-full bg-zinc-800 border-transparent focus:bg-zinc-700 focus:ring-2 focus:ring-amber-500/50 rounded-2xl p-4 transition-all" />
                </div>
              </div>
              <button className="w-full py-5 bg-amber-500 text-black font-extrabold rounded-2xl shadow-xl hover:bg-amber-400 transition-all flex items-center justify-center gap-3 active:scale-[0.98]">
                Confirmer par WhatsApp
              </button>
            </form>
          </div>
        )}

        {/* VIEW: CART */}
        {view === 'cart' && (
          <div className="max-w-5xl mx-auto space-y-10 animate-in slide-in-from-right-8 duration-700">
            <h1 className="text-5xl font-serif text-amber-500 text-center">Votre Sélection</h1>
            
            {cart.length === 0 ? (
              <div className="text-center py-24 bg-zinc-900/50 rounded-[3rem] border border-zinc-800/50 flex flex-col items-center">
                <div className="w-20 h-20 bg-zinc-800 rounded-full flex items-center justify-center text-zinc-600 mb-6">
                  <Icons.Cart />
                </div>
                <p className="text-zinc-500 text-xl mb-8">Votre panier est encore vide.</p>
                <button onClick={() => setView('menu')} className="px-8 py-3 bg-amber-500/10 border border-amber-500 text-amber-500 rounded-full font-bold hover:bg-amber-500 hover:text-black transition-all">
                  Découvrir nos plats
                </button>
              </div>
            ) : (
              <div className="grid lg:grid-cols-3 gap-10">
                <div className="lg:col-span-2 space-y-6">
                  {cart.map(item => (
                    <div key={item.id} className="flex flex-col sm:flex-row items-center gap-6 bg-zinc-900/60 p-6 rounded-3xl border border-zinc-800 group transition-all hover:bg-zinc-900">
                      <img src={item.image} className="w-28 h-28 rounded-2xl object-cover shadow-lg group-hover:scale-105 transition-transform" alt={item.name} />
                      <div className="flex-1 text-center sm:text-left">
                        <h4 className="text-xl font-bold font-serif">{item.name}</h4>
                        <p className="text-amber-500 font-bold">{item.price.toLocaleString()} FCFA</p>
                      </div>
                      <div className="flex items-center gap-4 bg-zinc-800 p-2 rounded-2xl">
                        <button onClick={() => updateQuantity(item.id, -1)} className="w-10 h-10 flex items-center justify-center rounded-xl bg-zinc-700 hover:bg-amber-500 hover:text-black transition-all font-bold">-</button>
                        <span className="w-8 text-center font-bold">{item.quantity}</span>
                        <button onClick={() => updateQuantity(item.id, 1)} className="w-10 h-10 flex items-center justify-center rounded-xl bg-zinc-700 hover:bg-amber-500 hover:text-black transition-all font-bold">+</button>
                      </div>
                      <button onClick={() => removeFromCart(item.id)} className="p-3 text-zinc-500 hover:text-red-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
                      </button>
                    </div>
                  ))}
                  <div className="p-8 bg-zinc-900/40 rounded-3xl border-2 border-dashed border-amber-500/20 flex justify-between items-center">
                    <span className="text-2xl font-serif">Total de la commande</span>
                    <span className="text-3xl font-bold text-amber-500">{cartTotal.toLocaleString()} FCFA</span>
                  </div>
                </div>

                <div className="bg-zinc-900 p-8 rounded-[2.5rem] border border-white/5 h-fit shadow-2xl sticky top-28">
                  <h3 className="text-2xl mb-8 font-serif font-bold text-amber-500">Validation Express</h3>
                  <form onSubmit={handleCheckout} className="space-y-6">
                    <div className="space-y-3">
                      <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest">Type de service</label>
                      <select name="type" className="w-full bg-zinc-800 p-4 rounded-2xl border-transparent focus:ring-2 focus:ring-amber-500/50">
                        <option value="Sur place">À Table (Sur place)</option>
                        <option value="Livraison">Livraison à domicile</option>
                      </select>
                    </div>
                    <div className="space-y-3">
                      <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest">N° Table ou Adresse précise</label>
                      <textarea name="logistics" required className="w-full bg-zinc-800 p-4 rounded-2xl border-transparent focus:ring-2 focus:ring-amber-500/50 min-h-[120px]" placeholder="Précisez votre emplacement ici..." />
                    </div>
                    <button className="w-full py-5 bg-green-500 text-white font-extrabold rounded-2xl shadow-xl hover:bg-green-600 transition-all flex items-center justify-center gap-3 active:scale-[0.98]">
                      Envoyer la Commande
                    </button>
                    <p className="text-[10px] text-zinc-500 text-center uppercase tracking-tighter">Votre commande sera envoyée directement sur notre WhatsApp officiel.</p>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        {/* VIEW: ADMIN */}
        {view === 'admin' && (
          <div className="max-w-6xl mx-auto space-y-12 animate-in slide-in-from-top-8 duration-700">
            <h1 className="text-5xl font-serif text-amber-500 text-center">Pilotage Gérant</h1>
            
            {adminCode !== ADMIN_PASS ? (
              <div className="max-w-md mx-auto text-center bg-zinc-900 p-10 rounded-[2.5rem] border border-zinc-800 space-y-6 shadow-2xl">
                <div className="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto text-amber-500">
                  <Icons.Admin />
                </div>
                <h3 className="text-2xl font-serif">Accès Réservé</h3>
                <input 
                  type="password" 
                  placeholder="Entrez votre code secret" 
                  onChange={(e) => setAdminCode(e.target.value)}
                  className="w-full bg-zinc-800 p-4 rounded-2xl border-transparent text-center focus:ring-2 focus:ring-amber-500/50 text-xl font-bold tracking-widest"
                />
              </div>
            ) : (
              <div className="grid lg:grid-cols-2 gap-12">
                <div className="space-y-8">
                  <h2 className="text-3xl font-serif text-amber-500 flex items-center gap-3">
                    <span className="p-2 bg-amber-500/10 rounded-xl"><Icons.Menu /></span> Gestion de la Carte
                  </h2>
                  <form className="bg-zinc-900 p-8 rounded-[2rem] border border-zinc-800 space-y-5" onSubmit={(e) => {
                    e.preventDefault();
                    const d = new FormData(e.currentTarget);
                    const newItem: MenuItem = {
                      id: Math.random().toString(36).substr(2, 9),
                      name: d.get('name') as string,
                      price: Number(d.get('price')),
                      description: d.get('desc') as string,
                      image: (d.get('img') as string) || 'https://via.placeholder.com/400x250',
                      category: 'Plat'
                    };
                    setMenu([...menu, newItem]);
                    e.currentTarget.reset();
                  }}>
                    <input name="name" placeholder="Nom du délice" required className="w-full bg-zinc-800 p-4 rounded-xl" />
                    <input name="price" type="number" placeholder="Prix (FCFA)" required className="w-full bg-zinc-800 p-4 rounded-xl" />
                    <input name="img" placeholder="URL de la photo" className="w-full bg-zinc-800 p-4 rounded-xl" />
                    <textarea name="desc" placeholder="Description savoureuse..." className="w-full bg-zinc-800 p-4 rounded-xl min-h-[100px]" />
                    <button className="w-full py-4 bg-amber-500 text-black font-extrabold rounded-xl hover:bg-amber-400 transition-all">
                      Ajouter à la Carte
                    </button>
                  </form>
                  
                  <div className="bg-zinc-900/50 p-6 rounded-[2rem] border border-zinc-800 max-h-[500px] overflow-y-auto no-scrollbar">
                    {menu.map(m => (
                      <div key={m.id} className="flex items-center gap-4 bg-zinc-800/50 p-4 rounded-2xl mb-3 group">
                        <img src={m.image} className="w-16 h-16 object-cover rounded-xl" alt={m.name} />
                        <div className="flex-1 min-w-0">
                          <p className="font-bold truncate">{m.name}</p>
                          <p className="text-amber-500 text-xs">{m.price.toLocaleString()} FCFA</p>
                        </div>
                        <button onClick={() => setMenu(menu.filter(i => i.id !== m.id))} className="text-zinc-600 hover:text-red-500 p-2">
                          <Icons.Call /> {/* Utiliser une icône générique ou définir Trash */}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-8">
                  <h2 className="text-3xl font-serif text-amber-500 flex items-center gap-3">
                    <span className="p-2 bg-amber-500/10 rounded-xl"><Icons.Reserve /></span> Flux Commandes
                  </h2>
                  <div className="space-y-5 h-full">
                    {orders.length === 0 ? (
                      <div className="bg-zinc-900/30 p-12 rounded-[2rem] border-2 border-dashed border-zinc-800 text-center text-zinc-600 italic">
                        En attente de commandes...
                      </div>
                    ) : orders.map(order => (
                      <div key={order.id} className="bg-zinc-900 p-6 rounded-[2rem] border border-zinc-800 relative group overflow-hidden">
                        <div className="absolute top-0 right-0 w-1 h-full bg-amber-500 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <span className="text-xs bg-zinc-800 px-3 py-1 rounded-full text-zinc-400">{new Date(order.timestamp).toLocaleTimeString()}</span>
                            <p className="text-xl font-bold mt-2 text-amber-500">{order.total.toLocaleString()} FCFA</p>
                          </div>
                          <div className="px-3 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-500 text-[10px] font-bold rounded-lg uppercase tracking-tighter">
                            {order.type}
                          </div>
                        </div>
                        <div className="space-y-3">
                            <div className="bg-black/20 p-3 rounded-xl">
                                {order.items.map((i, idx) => (
                                    <div key={idx} className="flex justify-between text-sm py-1 border-b border-zinc-800 last:border-0">
                                        <span>{i.name} <span className="text-zinc-500">x{i.quantity}</span></span>
                                        <span className="font-mono">{(i.price * i.quantity).toLocaleString()}</span>
                                    </div>
                                ))}
                            </div>
                            <p className="text-xs text-zinc-500 bg-zinc-800/40 p-3 rounded-xl italic">📍 {order.logistics}</p>
                        </div>
                      </div>
                    ))}
                    {orders.length > 0 && (
                      <button 
                        onClick={() => { if(confirm("Vider l'historique ?")) setOrders([]) }} 
                        className="w-full py-3 text-red-500 text-xs uppercase font-bold hover:bg-red-500/5 rounded-xl transition-colors mt-4"
                      >
                        Vider l'Historique
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="py-12 border-t border-zinc-900/50 mt-16 bg-zinc-900/20 text-center text-zinc-500 text-xs tracking-widest uppercase">
        <p>© 2024 Teranga Gourmet Dakar • L'art du Bien-Recevoir</p>
        <div className="flex justify-center gap-6 mt-6">
          <a href={`tel:${CALL_NUMBER}`} className="text-amber-500 font-bold hover:underline">{CALL_NUMBER}</a>
          <span className="text-zinc-800">|</span>
          <span className="text-zinc-600">Ouvert 7j/7 • 12h - 00h</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
