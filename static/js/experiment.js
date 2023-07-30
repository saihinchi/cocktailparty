
//音声を一回だけ流すやつ
window.addEventListener('load', function(){
	var option = {
	once: true
	};
	document.getElementById("RRR").addEventListener('click', RanRan);});



function RanRan()
{
    document.getElementById("sound").load();
    document.getElementById("sound").play();
    this.removeEventListener("click",RanRan);
}

//文字追加するやつ
function addTF(str)
{
	document.faceForm.face.value = str;
  document.faceForm.time.value = document.getElementById("watchArea").innerHTML;
}

//練習問題で正解を表示させるやつ
var display=function() {
    //切り替える対象の状態を取得
    var div = document.getElementById('view');
    //取得した情報からスタイルについての状態のみをstateに代入
    state=div.style.display;
    //デバッグ用にlogに出力
    console.log(state);
    //非表示中のときの処理
    if(state=="none"){
         //スタイルを表示(inline)に切り替え
         div.setAttribute("style","display:inline");
        //デバッグ用にinlineをlogに出力
        console.log("inline");
    }else{
         //スタイルを非表示(none)に切り替え
        div.setAttribute("style","display:none");
        //デバッグ用にnoneをlogに出力
        console.log("none");
    }
}



//時間を測るやつ
"use strict";
 
 window.addEventListener( "DOMContentLoaded" , ()=> {
     /**
      * @param watchCallBack 経過時間報告用コールバック
      */
     const getStopWatch = function ( watchCallBack ){
         let accumulatedTime = 0,    // 積算時間
             currentTime=null,       // タイマー開示タイムスタンプ
             timerId=null;           // setInterval() の返り値
  
             // リセット処理
         const reset = () =>{
             timerOff(); accumulatedTime = 0; currentTime=null;
                 // リセットされたことをnullで通知
             watchCallBack( null ); 
         };
             // 開始処理
         const start = () =>{ currentTime = Date.now();timerOn(); };
             // 一時停止処理
         const pause = () =>{
                 // これまでの経過時間を退避
             accumulatedTime = getNowTime();
             timerOff();
             currentTime = null;
         };

      
             // 経過時間の算出
         const getNowTime = () =>accumulatedTime + Date.now() - currentTime;
  
             // タイマー停止処理
         const timerOff = () => {
             if( timerId === null ) return;
             clearInterval(timerId);
             timerId = null;
         };
             // タイマー開始処理
         const timerOn = () => {
             if( timerId !== null ) clearTimeout(timerId);
             timerId = setInterval(()=>watchCallBack( getNowTime() ),10);
         };
  
         reset();
  
             // 必要な機能だけ返す
         return Object.freeze({
             start:()=> currentTime === null && accumulatedTime === 0 ?   start()  : reset(),
             pause:()=> currentTime === null ? ( accumulatedTime === 0 ? false : resume() ) : pause(),
         });
     };
  
         // ミリ秒を画面表示する形式に変換
     const timeString = time =>`${
         Math.floor(time / 60000).toString().padStart(2,"00")
     }:${
         Math.floor(time % 60000 / 1000).toString().padStart(2,"00")
     }.${
         Math.floor(time % 1000).toString().padStart(3,"000").slice(0,2)
     }`;
  
     const watchArea = document.getElementById("watchArea");

  
     const stopWatchObj = getStopWatch(
          time => watchArea.textContent = time === null ? "00:00.00" : timeString( time ) ,
     );
  
     const buttonDefine = [
             { id:"RRR" , listener:()=>stopWatchObj.start() },
             { id:"P" , listener:()=>stopWatchObj.pause() },

         ];
     buttonDefine.forEach( e => document.getElementById(e.id).addEventListener("click",e.listener));
 });

