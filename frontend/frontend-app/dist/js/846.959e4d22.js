"use strict";(self["webpackChunkfrontend_app"]=self["webpackChunkfrontend_app"]||[]).push([[846],{846:function(e,l,o){o.r(l),o.d(l,{default:function(){return b}});var r=o(6768),a=o(5130);const n={class:"login-container"},t={key:0,class:"login-error"},u={class:"back-to-home"};function i(e,l,o,i,s,d){const g=(0,r.g2)("el-input"),m=(0,r.g2)("el-form-item"),p=(0,r.g2)("el-alert"),c=(0,r.g2)("el-button"),b=(0,r.g2)("router-link"),f=(0,r.g2)("el-form"),k=(0,r.g2)("el-card");return(0,r.uX)(),(0,r.CE)("div",n,[(0,r.bF)(k,{class:"login-card"},{header:(0,r.k6)((()=>l[2]||(l[2]=[(0,r.Lk)("div",{class:"login-header"},[(0,r.Lk)("h2",null,"管理员登录"),(0,r.Lk)("p",null,"窗帘样本管理系统")],-1)]))),default:(0,r.k6)((()=>[(0,r.bF)(f,{ref:"loginFormRef",model:i.loginForm,rules:i.loginRules,"label-position":"top",onSubmit:(0,a.D$)(i.handleLogin,["prevent"])},{default:(0,r.k6)((()=>[(0,r.bF)(m,{label:"用户名",prop:"username"},{default:(0,r.k6)((()=>[(0,r.bF)(g,{modelValue:i.loginForm.username,"onUpdate:modelValue":l[0]||(l[0]=e=>i.loginForm.username=e),"prefix-icon":"el-icon-user",placeholder:"请输入管理员用户名",clearable:""},null,8,["modelValue"])])),_:1}),(0,r.bF)(m,{label:"密码",prop:"password"},{default:(0,r.k6)((()=>[(0,r.bF)(g,{modelValue:i.loginForm.password,"onUpdate:modelValue":l[1]||(l[1]=e=>i.loginForm.password=e),"prefix-icon":"el-icon-lock",type:"password",placeholder:"请输入密码","show-password":""},null,8,["modelValue"])])),_:1}),i.authStore.error?((0,r.uX)(),(0,r.CE)("div",t,[(0,r.bF)(p,{title:i.authStore.error,type:"error","show-icon":""},null,8,["title"])])):(0,r.Q3)("",!0),(0,r.bF)(m,null,{default:(0,r.k6)((()=>[(0,r.bF)(c,{type:"primary","native-type":"submit",loading:i.authStore.loading,class:"login-button"},{default:(0,r.k6)((()=>l[3]||(l[3]=[(0,r.eW)(" 登录 ")]))),_:1},8,["loading"])])),_:1}),(0,r.Lk)("div",u,[(0,r.bF)(b,{to:{name:"Home"}},{default:(0,r.k6)((()=>l[4]||(l[4]=[(0,r.eW)("返回前台首页")]))),_:1})])])),_:1},8,["model","rules","onSubmit"])])),_:1})])}o(4114);var s=o(144),d=o(1387),g=o(6191),m={name:"Login",setup(){const e=(0,d.rd)(),l=(0,g.n)(),o=(0,s.KR)(null),r=(0,s.Kh)({username:"",password:""}),a={username:[{required:!0,message:"请输入用户名",trigger:"blur"},{min:3,max:20,message:"用户名长度应为3-20个字符",trigger:"blur"}],password:[{required:!0,message:"请输入密码",trigger:"blur"},{min:6,message:"密码长度不能少于6个字符",trigger:"blur"}]},n=async()=>{o.value&&await o.value.validate((async o=>{if(o){const o=await l.login(r);o&&e.push({name:"Admin"})}}))};return{loginForm:r,loginRules:a,loginFormRef:o,authStore:l,handleLogin:n}}},p=o(1241);const c=(0,p.A)(m,[["render",i],["__scopeId","data-v-673ca954"]]);var b=c}}]);
//# sourceMappingURL=846.959e4d22.js.map