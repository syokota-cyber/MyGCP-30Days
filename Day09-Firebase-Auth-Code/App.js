import React, { useState, useEffect } from 'react';
import { auth } from './firebase';
import { onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from 'firebase/auth';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isSignUp) {
        await createUserWithEmailAndPassword(auth, email, password);
        alert('アカウント作成成功！');
      } else {
        await signInWithEmailAndPassword(auth, email, password);
      }
    } catch (error) {
      alert('エラー: ' + error.message);
    }
  };

  const handleLogout = () => {
    signOut(auth);
  };

  if (loading) return <div style={{textAlign:'center', marginTop:'50px'}}>読み込み中...</div>;

  return (
    <div className="App">
      {user ? (
        <div style={{textAlign:'center', marginTop:'50px'}}>
          <h2>🎉 Day9 目標達成！</h2>
          <h3>認証済みユーザー限定ページ</h3>
          <p>ようこそ、{user.email}さん！</p>
          <p>このページはログインした人だけが見ることができます✨</p>
          <button onClick={handleLogout} style={{padding:'10px 20px', fontSize:'16px', marginTop:'20px'}}>
            ログアウト
          </button>
        </div>
      ) : (
        <div style={{textAlign:'center', marginTop:'50px'}}>
          <h2>{isSignUp ? '新規登録' : 'ログイン'}</h2>
          <form onSubmit={handleSubmit} style={{maxWidth:'300px', margin:'0 auto'}}>
            <div style={{marginBottom:'15px'}}>
              <input
                type="email"
                placeholder="メールアドレス"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{width:'100%', padding:'10px', fontSize:'16px'}}
                required
              />
            </div>
            <div style={{marginBottom:'15px'}}>
              <input
                type="password"
                placeholder="パスワード（6文字以上）"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{width:'100%', padding:'10px', fontSize:'16px'}}
                required
              />
            </div>
            <button type="submit" style={{width:'100%', padding:'10px', fontSize:'16px', marginBottom:'10px'}}>
              {isSignUp ? '新規登録' : 'ログイン'}
            </button>
          </form>
          <button 
            onClick={() => setIsSignUp(!isSignUp)}
            style={{background:'none', border:'none', color:'blue', textDecoration:'underline', cursor:'pointer'}}
          >
            {isSignUp ? 'ログインに切り替え' : '新規登録に切り替え'}
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
