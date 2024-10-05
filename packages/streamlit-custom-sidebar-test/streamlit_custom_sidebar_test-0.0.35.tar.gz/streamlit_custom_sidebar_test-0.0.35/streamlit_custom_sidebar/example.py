import streamlit as st

st.set_page_config(layout="wide")

from slim_expand_sidebar.__init__ import NoHoverExpandSidebarTemplate, HoverExpandSidebarTemplate #SidebarIcons, _sidebar_component #

# st.set_page_config()

# class NoHoverExpandSidebarTemplate:

#     """
#     Create your very own custom side bar navigation in streamlit with more ideal features. 

#     Args:
#         - (required) closedOnLoad: whether the sidebar should be closed when app first loads. Defaults to false
#         - (required) widthOfSidebar: width of the sidebar. Defaults to 300px.
#         - (optional) closeBtnColor: color of the close sidebar button. If "auto", it uses streamlit's text color, if not "auto" then specify a color.
#         - (optional) backgroundColor: background color of the sidebar
#         - (optional) activeBackgroundColor: background color of active/currently clicked page/tab
#         - (optional) navigationHoverBackgroundColor: color of navigation tab when you hover over it
#         - (optional) labelIconSize: font size of the text (label) and icon
#         - (optional) distanceIconLabel: distance between the icon and the label in the navigation tab
#         - (optional/required) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None. Though for some methods in the component, if you wish to use them, this is a requirement. Methods like change_page() and load_custom_sidebar()..
#         - (required) data: data used to build the side bar navigation:
#             args:
#                 - index: required 
#                 - label: required - name of the navigation tab. The is what you want it to appear as.
#                 - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
#                 - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
#                 - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"
#         - (optional) base_data: data used to build the base of the side bar navigation - settings, logout, socials etc:
#             args:
#                 - index: required 
#                 - label: required - name of the navigation tab. The is what you want it to appear as.
#                 - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
#                 - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
#                 - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"

#         - (optional) webMedium: Where is this page currently being displayed. Options: "local", "streamlit-cloud", "custom" - if you are using another service like AWS etc.
#         - (optional) iframeContainer: Used to find head tag to append icon libraries so that they can be displayed. This is required if webMedium is `custom`.
#     """

#     def __init__(self, closedOnLoad=False, widthOfSidebar="300px", closeBtnColor="auto", backgroundColor="black", activeBackgroundColor="white", navigationHoverBackgroundColor="rgba(255,255,255,1)", labelIconSizeNav="17px", labelIconSizeBase="16px", labelIconSizeFooter="16px", distanceIconLabel="15px", labelIconColorNotActive="#fff", labelIconColorActive="black", sizeOfCloseSidebarBtn="24px", loadPageName=None, logoUrl="", logoImg='https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y', logoImgWidth="49px", logoText="", logoTextColor="white", logoImgHeight="49px", logoTextSize="20px", logoTextDistance="10px", data=None, base_data=None, footer_data=None, headlineText=None, mainText=None, informationLink=None, webMedium="local", iframeContainer=None) -> None: 
        
#         self.logoUrl = logoUrl
#         self.closedOnLoad = closedOnLoad
#         self.widthOfSidebar = widthOfSidebar
#         self.closeBtnColor = closeBtnColor
#         self.backgroundColor = backgroundColor
#         self.activeBackgroundColor = activeBackgroundColor
#         self.navigationHoverBackgroundColor = navigationHoverBackgroundColor
#         self.labelIconSizeNav = labelIconSizeNav
#         self.labelIconSizeBase = labelIconSizeBase
#         self.labelIconSizeFooter = labelIconSizeFooter
#         self.distanceIconLabel = distanceIconLabel
#         self.labelIconColorNotActive = labelIconColorNotActive
#         self.labelIconColorActive = labelIconColorActive
#         self.sizeOfCloseSidebarBtn = sizeOfCloseSidebarBtn
#         self.loadPageName = loadPageName
#         self.logoImg = logoImg 
#         self.logoImgWidth = logoImgWidth
#         self.logoImgHeight = logoImgHeight
#         self.logoText = logoText
#         self.logoTextSize = logoTextSize
#         self.logoTextColor = logoTextColor
#         self.logoTextDistance = logoTextDistance
#         self.data = data
#         self.base_data = base_data
#         self.footer_data = footer_data
#         self.headlineText = headlineText
#         self.mainText = mainText
#         self.informationLink = informationLink
#         self.webMedium = webMedium
#         self.iframeContainer = iframeContainer

#     def sidebarCreate(self):
#         """
#         Sidebar creation component which creates the sidebar for the app.
#         """ 
#         if self.closeBtnColor != "auto":
#             closeBtnColor_ = self.closeBtnColor
#         else:
#             closeBtnColor_ = ""

#         if self.closedOnLoad:
#             className = "sidebar-section sidebar-closed"
#             width = "0px"
#             translateX = "-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px" 
#             close_icon = "menu"
#             padding = "0px"
#             margin="0px"
#         else:
#             className = "sidebar-section"
#             width = self.widthOfSidebar
#             translateX = "0px"
#             close_icon = "menu"
#             padding = "1rem 0.8rem"
#             margin="10px"
        
#         js_el = f'''
                                    
#                     <script>
                        
#                         const sidebar = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"]');
#                         if (sidebar.length < 1){{
                            
#                             const createEL = window.parent.document.createElement("section");
#                             createEL.className = 'custom-sidebar';
#                             createEL.style = "display:flex; z-index:999999;";
#                             createElSidebarSection = document.createElement("div");
#                             createElSidebarSection.className = "{className}";

#                             const closeSidebarSmallScreen = document.createElement("div");
#                             closeSidebarSmallScreen.className = "close-btn-small-screen";
#                             const closeSidebarSmallScreenIcon = document.createElement("i");
#                             closeSidebarSmallScreenIcon.id = "close-sidebar-btn-icon"; 
#                             closeSidebarSmallScreenIcon.className = 'material-symbols-outlined';
#                             closeSidebarSmallScreenIcon.innerText = '{close_icon}';
#                             closeSidebarSmallScreenIcon.style.color = "{closeBtnColor_}";
#                             closeSidebarSmallScreen.style = 'visibility:hidden; color:white !important;';
#                             closeSidebarSmallScreen.appendChild(closeSidebarSmallScreenIcon)
                            
#                             createElSidebarSection.style = 'display:flex; flex-direction:column; position:relative; padding: {padding}; height: 97.5vh; margin: {margin}; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; cursor:pointer; overflow:hidden; width: {width}; transform: translateX({translateX}); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
#                             createEL.appendChild(createElSidebarSection);

#                             const sidebarCloseBtnContainer = document.createElement("div");
#                             sidebarCloseBtnContainer.className = "close-sidebar-btn-container"
#                             sidebarCloseBtnContainer.style = "visibility:visible; padding: 4px; border-radius: 4px; width: fit-content; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer;";
                            
#                             const mainPageLogo = document.createElement("a");
#                             const sidebarCloseBtn = document.createElement("div");
#                             sidebarCloseBtn.className = "close-sidebar-btn"
#                             sidebarCloseBtn.style = "font-size: {self.sizeOfCloseSidebarBtn};";
#                             const sidebarCloseBtnIcon = document.createElement("i");
#                             sidebarCloseBtnIcon.id = "close-sidebar-btn-icon"
#                             sidebarCloseBtnIcon.className = 'material-symbols-outlined';
#                             sidebarCloseBtnIcon.innerText = '{close_icon}';
#                             sidebarCloseBtnIcon.style.color = "{closeBtnColor_}";

#                             sidebarCloseBtn.appendChild(sidebarCloseBtnIcon);
#                             sidebarCloseBtnContainer.appendChild(sidebarCloseBtn);


#                             createEL.appendChild(sidebarCloseBtnContainer); 
                            
#                             const body = window.parent.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
#                             body[0].insertAdjacentElement('beforebegin',createEL);

#                             const newSidebar = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="{className}"]');
#                             const logoImgContainer = document.createElement("div");   
#                             logoImgContainer.style = 'display:flex; justify-content:space-between;';
#                             const logoImgLink = document.createElement("a");
#                             logoImgLink.href = '{self.logoUrl}'; 
#                             logoImgLink.style = 'text-decoration:none; width:fit-content; height:50px; display:flex; justify-content:center; align-items:center;';                 
#                             //logoImgContainer.style = 'width:fit-content; height:50px; display:flex; justify-content:center; align-items:center;';                 

#                             const logoImg = document.createElement("img");
#                             logoImg.className = "logo-img";
#                             logoImg.src = '{self.logoImg}'; 
#                             logoImg.setAttribute("width", "{self.logoImgWidth}");
#                             logoImg.setAttribute("height", "{self.logoImgHeight}");   

#                             const logoTextDiv = document.createElement("div");
#                             logoTextDiv.className = "logo-text";
#                             logoTextDiv.innerText = '{self.logoText}';  
#                             logoTextDiv.style = "font-size: {self.logoTextSize}; color:{self.logoTextColor}; margin-left:{self.logoTextDistance}; white-space:nowrap;";           
                            

#                             logoImgLink.append(logoImg)
#                             logoImgLink.append(logoTextDiv)
#                             logoImgContainer.append(logoImgLink)
#                             logoImgContainer.appendChild(closeSidebarSmallScreen) 
#                             //logoImgContainer.appendChild(logoImg); 
#                             //logoImgContainer.appendChild(logoTextDiv); 
#                             newSidebar[0].appendChild(logoImgContainer); 

#                             const lineDivy = document.createElement('div');
#                             lineDivy.className = "divy-line-logo-nav-container";
#                             const line = document.createElement('hr');
#                             line.className="divy-line";
#                             line.style = "border-top: 0.2px solid #bbb;";
#                             lineDivy.appendChild(line);
#                             newSidebar[0].appendChild(lineDivy);

#                             const navigationTabsContainer = document.createElement('ul');
#                             navigationTabsContainer.className = "navigation-selections-container";
#                             navigationTabsContainer.style = 'list-style-type:none; padding-left:0px; display:flex; flex-direction:column; width:100%; row-gap:5px;';  

#                             var pageName_ = window.parent.document.location.pathname.split("/");  
#                             var pageName_ = pageName_[pageName_.length - 1];   

#                             if (pageName_ == ""){{
#                                 pageName_ = {self.data}[0]["page_name"];
#                             }} 
                            

#                             {self.data}.forEach((el) => {{
#                                 const createListEl = document.createElement('li');
#                                 createListEl.className = "label-icon-container";  
#                                 createListEl.style.borderRadius = "4px";
                                
#                                 const navTabContent = document.createElement('div');
#                                 navTabContent.className = "contents-container";
#                                 navTabContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:40px;";
                                
#                                 const iconEl = document.createElement('i');
#                                 iconEl.style.fontSize = "{self.labelIconSizeNav}";
#                                 iconEl.id = 'sidebar-element-icons';

#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     iconEl.className = el.icon;
                                    
                                    
#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                    
#                                     iconEl.className = 'material-symbols-outlined';
#                                     iconEl.innerText = el.icon;
                                    
#                                 }}

#                                 const labelEl = document.createElement('div');
#                                 labelEl.className = "navigation-label";
#                                 labelEl.dataset.testid = el.page_name;
#                                 labelEl.innerHTML = el.label;
#                                 labelEl.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeNav}; margin-left:{self.distanceIconLabel}; width:100%;";
                                
#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style.backgroundColor = '{self.activeBackgroundColor}'; 
#                                         iconEl.style.color = "{self.labelIconColorActive}";
#                                         labelEl.style.color = "{self.labelIconColorActive}";
#                                     }} else {{
#                                         iconEl.style.color = "{self.labelIconColorNotActive}";
#                                         labelEl.style.color = "{self.labelIconColorNotActive}";
                                        
#                                     }}
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         iconEl.style.color = "{self.labelIconColorActive}";
#                                         labelEl.style.color = "{self.labelIconColorActive}";
                                        
#                                     }}  else {{
#                                         iconEl.style.color = "{self.labelIconColorNotActive}";
#                                         labelEl.style.color = "{self.labelIconColorNotActive}";
#                                     }}

#                                 }}

#                                 navTabContent.appendChild(iconEl);                                
#                                 navTabContent.appendChild(labelEl);
#                                 createListEl.appendChild(navTabContent);                                    
#                                 navigationTabsContainer.appendChild(createListEl);

#                             }})

#                             newSidebar[0].appendChild(navigationTabsContainer);

#                             const informationalBar = document.createElement("a");
#                             informationalBar.className = "information-bar-section"
#                             informationalBar.style = 'display:flex; flex-direction:column; align-items:center; height:100px; width: 100%; background-color:#505050; border-radius:4px; margin-top:auto; margin-bottom:20px; text-decoration:none;';
#                             informationalBar.href = '{self.informationLink}';
#                             informationalBar.target = '_blank';
#                             const textBarContainer = document.createElement("div");
#                             textBarContainer.className = 'text-content';
#                             textBarContainer.style = 'color:white; font-size:10px; text-align:left; width: calc(90% - 1px); margin-bottom: 7px; margin-top:10px;';
#                             textBarContainer.innerHTML = '{self.headlineText}'; 
#                             informationalBar.appendChild(textBarContainer);
#                             const barContentContainer = document.createElement("div");
#                             barContentContainer.className = 'bar-container';
#                             barContentContainer.style = 'height:9px; position:relative; width:calc(90% - 1px); background-color:#8F8F8F; border-radius:11px;';
#                             const barContent = document.createElement("div");
#                             barContent.style = 'width: 50%; height:100%; background-color:white; border-radius:11px;'; 
#                             barContentContainer.appendChild(barContent)
#                             const mainTextContainer = document.createElement("div");
#                             mainTextContainer.style = 'display:flex; justify-content:space-between; width:calc(90% - 1px); margin:auto; align-items:center;';
#                             const mainText = document.createElement("div");
#                             mainText.style = 'color:white; text-align:left; width:calc(90% - 1px); font-size:12px;';
#                             mainText.innerHTML = '{self.mainText}';
#                             const iconToDirect = document.createElement("span");
#                             iconToDirect.className = 'material-symbols-outlined'; 
#                             iconToDirect.innerHTML = 'chevron_right';
#                             iconToDirect.style = 'color:white; font-size:16px;';

#                             mainTextContainer.appendChild(mainText)
#                             mainTextContainer.appendChild(iconToDirect)

                            
#                             informationalBar.appendChild(barContentContainer);
#                             informationalBar.appendChild(mainTextContainer);
#                             newSidebar[0].appendChild(informationalBar);


#                             const logoutBtnContainer = document.createElement("div");
#                             logoutBtnContainer.className = "navigation-selections-container";
#                             logoutBtnContainer.style = 'display:flex; flex-direction:column; width:100%; row-gap:1px;';


#                             {self.base_data}.length > 0 && {self.base_data}.forEach((el) => {{ 
                                                                                    
#                                 const baseContainer = document.createElement("div");
#                                 baseContainer.className = "label-icon-container";
#                                 baseContainer.style.borderRadius = "4px";

#                                 const baseContainerContent = document.createElement('div');
#                                 baseContainerContent.className = "contents-container";
#                                 baseContainerContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:38px;";

#                                 const baseContainerIcon = document.createElement("i");
#                                 baseContainerIcon.id = 'sidebar-element-icons'; 
#                                 baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";

#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     baseContainerIcon.className = el.icon;                                    
                                    
#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                    
#                                     baseContainerIcon.className = 'material-symbols-outlined';
#                                     baseContainerIcon.innerText = el.icon;
                                    
#                                 }}

#                                 const baseContainerLabel = document.createElement("div");
#                                 baseContainerLabel.className = "navigation-label";  
#                                 baseContainerLabel.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeBase}; margin-left:{self.distanceIconLabel}; width:100%;";
#                                 baseContainerLabel.innerText = el.label;
#                                 baseContainerLabel.dataset.testid = el.page_name;
                                
                                
#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         baseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         baseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{
                                        
#                                         baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         baseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         baseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{

#                                         baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}

#                                 }}
                                
#                                 baseContainerContent.appendChild(baseContainerIcon)
#                                 baseContainerContent.appendChild(baseContainerLabel);
#                                 baseContainer.appendChild(baseContainerContent);
#                                 logoutBtnContainer.appendChild(baseContainer);

#                             }})
 
#                             newSidebar[0].appendChild(logoutBtnContainer);

#                             const footerLogoutBtnContainer = document.createElement("div");
#                             footerLogoutBtnContainer.className = "footer-navigation-selections-container";
#                             footerLogoutBtnContainer.style = 'display:flex; flex-direction:row; width:100%; column-gap:1px; justify-content:flex-start; align-items:center; margin-top:25px;';

#                             {self.footer_data}.length > 0 && {self.footer_data}.forEach((el) => {{ 
                                                                                    
#                                 const footerBaseContainer = document.createElement("a");
#                                 footerBaseContainer.className = "footer-label-icon-container";
#                                 footerBaseContainer.style.borderRadius = "4px";
#                                 footerBaseContainer.style.textDecoration = "none";
#                                 footerBaseContainer.href = el.href;
#                                 footerBaseContainer.target = '_blank';

#                                 const footerBaseContainerContent = document.createElement('div');
#                                 footerBaseContainerContent.className = "footer-contents-container";
#                                 footerBaseContainerContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:25px;";

#                                 const footerBaseContainerIcon = document.createElement("i");
#                                 footerBaseContainerIcon.id = 'footer-sidebar-element-icons'; 
#                                 footerBaseContainerIcon.style.fontSize = "{self.labelIconSizeFooter}";

#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     footerBaseContainerIcon.className = el.icon;                                    
                                    
#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                    
#                                     footerBaseContainerIcon.className = 'material-symbols-outlined';
#                                     footerBaseContainerIcon.innerText = el.icon;
                                    
#                                 }}

#                                 const footerBaseContainerLabel = document.createElement("div");
#                                 footerBaseContainerLabel.className = "footer-navigation-label";  
#                                 footerBaseContainerLabel.style = "white-space:nowrap; display:table-cell; font-size:'{self.labelIconSizeFooter}'; margin-left:6px; width:100%;";
#                                 footerBaseContainerLabel.innerText = el.label;
#                                 footerBaseContainerLabel.dataset.testid = el.page_name;
                                
                                
#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         footerBaseContainer.id = "active-element";   
#                                         footerBaseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         footerBaseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         footerBaseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{
                                        
#                                         footerBaseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         footerBaseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         footerBaseContainer.id = "active-element";   
#                                         footerBaseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         footerBaseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         footerBaseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{

#                                         footerBaseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         footerBaseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}

#                                 }}
                                
#                                 footerBaseContainerContent.appendChild(footerBaseContainerIcon)
#                                 footerBaseContainerContent.appendChild(footerBaseContainerLabel);
#                                 footerBaseContainer.appendChild(footerBaseContainerContent);
#                                 footerLogoutBtnContainer.appendChild(footerBaseContainer);

#                             }})

#                             newSidebar[0].appendChild(footerLogoutBtnContainer)
                            
#                         }}
                    
#                     </script> 

#                 '''
        
#         st.components.v1.html(js_el, height=0, width=0) 
    
#     def hover_over_siebar_navigations(self):

#         js_el = f'''
#                     <script>

#                         const navigationBtn = window.parent.document.querySelectorAll(".label-icon-container");
#                         navigationBtn.forEach((c) => {{
#                             c.addEventListener('mouseover', function(e) {{ 
                                
#                                 e.preventDefault();
#                                 c.style.backgroundColor = '{self.navigationHoverBackgroundColor}'; 

#                                 const textLabel = c.querySelectorAll(".navigation-label");
#                                 textLabel[0].style.color = '{self.labelIconColorActive}';
#                                 const textIcon = c.querySelectorAll("#sidebar-element-icons");
#                                 textIcon[0].style.color = '{self.labelIconColorActive}';
#                                 c.style.borderRadius = '4px';
                                
                                
#                             }})

#                             c.addEventListener('mouseout', function(e) {{ 
                                
#                                 e.preventDefault();
#                                 const textLabel = c.querySelectorAll(".navigation-label");
#                                 const textIcon = c.querySelectorAll("#sidebar-element-icons");
#                                 c.style.borderRadius = '4px';

#                                 if (c.id === "active-element"){{
#                                     c.style.backgroundColor = '{self.activeBackgroundColor}';
#                                     textLabel[0].style.color = '{self.labelIconColorActive}';
#                                     textIcon[0].style.color = '{self.labelIconColorActive}';
#                                 }} else {{
#                                     c.style.backgroundColor = "transparent";
#                                     textLabel[0].style.color = '{self.labelIconColorNotActive}';
#                                     textIcon[0].style.color = '{self.labelIconColorNotActive}';
#                                 }}
                                                                
#                             }})

#                         }})
#                     </script>
#                 '''
#         st.components.v1.html(js_el, height=0, width=0)

#     def active_navigation(self):
#         """
#             Configures the active navigation tabs - adds `active-element` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
#         """

#         js_el = f'''
                    
#                     <script>
#                         var navigationTabs = window.parent.document.querySelectorAll(".custom-sidebar > .sidebar-section > .navigation-selections-container > .label-icon-container"); 
#                         navigationTabs.forEach((c) => {{
#                             c.addEventListener("click", (e) => {{
                                
#                                 window.parent.document.querySelectorAll('#active-element')[0]?.removeAttribute('style');
#                                 window.parent.document.querySelectorAll('#active-element')[0]?.removeAttribute('id'); 
#                                 c.id = "active-element";
#                                 c.style.backgroundColor = "{self.activeBackgroundColor}";
#                                 c.style.borderRadius = "4px";

#                                 const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
#                                 icons_[0].style.color = "{self.labelIconColorActive}";
#                                 const label_ = c.querySelectorAll(".contents-container > .navigation-label")
#                                 label_[0].style.color = "{self.labelIconColorActive}";

#                                 var newNavigationTabs = window.parent.document.querySelectorAll(".custom-sidebar > .sidebar-section > .navigation-selections-container > .label-icon-container"); 
#                                 newNavigationTabs.forEach((c) => {{ 
                                    
                                    
#                                     if (c.id !== "active-element"){{
#                                         const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
#                                         icons_[0].style.color = "{self.labelIconColorNotActive}";
#                                         const label_ = c.querySelectorAll(".contents-container > .navigation-label")
#                                         label_[0].style.color = "{self.labelIconColorNotActive}";
#                                     }}
#                                 }})

#                             }});
                           
#                         }});

#                         let iframeScreenComp = window.parent.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
#                         iframeScreenComp[0].parentNode.style.display = "none";
                        
#                     </script>

#                 '''
#         st.components.v1.html(js_el, height=0, width=0)
      
#     def close_sidebar(self):

#         js_el_ = f'''
#                     <script>
#                         function changeClassNameForSidebar (event) {{
                            
#                             const sidebarSectionOpen = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

#                             if (sidebarSectionOpen.length > 0){{
#                                 sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
#                                 sidebarSectionOpen[0].style = 'display:flex; flex-direction:column; width: 0px; padding: 0px; margin:0px; transform: translateX({"-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px"}); transition: all 300ms ease 0s;'; // transform 300ms ease 0s;'; //, width 300ms ease 0s;';        
                                
#                             }} else {{
#                                 const sidebarSectionClosed = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
#                                 sidebarSectionClosed[0].className = "sidebar-section"
#                                 sidebarSectionClosed[0].style = 'display:flex; flex-direction:column; position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; cursor:pointer; overflow:hidden; width: {self.widthOfSidebar}; transform: translateX(0px); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                    
#                             }}
#                             event.preventDefault();
#                         }}

#                         const sidebarSectionCloseBtn = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
#                         sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
#                     </script> 

#                     '''
#         st.components.v1.html(js_el_, height=0, width=0) 
    
#     def closed_btn_small_screen(self):

#         js_el_ = f'''
#                     <script>

#                         let current_screen_size = window.parent.matchMedia("(max-width: 768px)"); 

#                         function changeCloseBtnOnSmallScreen (event) {{
                            
#                             const sidebarOpenCloseBtn = window.parent.document.body.querySelectorAll('div[class="close-sidebar-btn-container"]');
#                             const smallScreenSidebarCloseBtn = window.parent.document.body.querySelectorAll('div[class="close-btn-small-screen"]');

#                             if (current_screen_size.matches){{
#                                 sidebarOpenCloseBtn[0].style = 'position:fixed; left: 1.25rem; top: 1.25rem; z-index:-1; padding: 4px; border-radius: 4px; width: fit-content; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer;';
#                                 smallScreenSidebarCloseBtn[0].style = 'visibility:visible; color:white !important;';
#                             }} else {{
#                                 sidebarOpenCloseBtn[0].style = 'visibility:visible; padding: 4px; border-radius: 4px; width: fit-content; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;';
#                                 smallScreenSidebarCloseBtn[0].style = 'visibility:hidden; color:white !important;';
#                             }}
                            
#                             event.preventDefault();
#                         }}

#                         current_screen_size.addEventListener("change", changeCloseBtnOnSmallScreen);
   
                        
#                     </script> 
#                 '''
#         st.components.v1.html(js_el_, height=0, width=0) 

#     def closed_btn_small_screen_first_load(self):

#         js_el_ = f'''
#                     <script>

#                         let current_screen_size = window.parent.matchMedia("(max-width: 768px)"); 

#                         function changeCloseBtnOnSmallScreen (event) {{
                            
#                             const sidebarOpenCloseBtn = window.parent.document.body.querySelectorAll('div[class="close-sidebar-btn-container"]');
#                             const smallScreenSidebarCloseBtn = window.parent.document.body.querySelectorAll('div[class="close-btn-small-screen"]');

#                             if (current_screen_size.matches){{
#                                 sidebarOpenCloseBtn[0].style = 'position:fixed; left: 1.25rem; top: 1.25rem; z-index:-1; padding: 4px; border-radius: 4px; width: fit-content; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer;';
#                                 smallScreenSidebarCloseBtn[0].style = 'visibility:visible; color:white !important;';
#                             }} else {{
#                                 sidebarOpenCloseBtn[0].style = 'visibility:visible;  padding: 4px; border-radius: 4px; width: fit-content; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;';
#                                 smallScreenSidebarCloseBtn[0].style = 'visibility:hidden; color:white !important;';
#                             }}
                            
#                             event.preventDefault();
#                         }}

#                         changeCloseBtnOnSmallScreen() 
                        
#                     </script> 
#                 '''
#         st.components.v1.html(js_el_, height=0, width=0) 

#     def close_sidebar_small_screen(self):

#         js_el_ = f'''
#                     <script>
#                         function changeClassNameForSidebar (event) {{
                            
#                             const sidebarSectionOpen = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

#                             if (sidebarSectionOpen.length > 0){{
#                                 sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
#                                 sidebarSectionOpen[0].style = 'width: 0px; padding: 0px; margin:0px; transform: translateX({"-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px"}); transition: transform 300ms ease 0s, width 300ms ease 0s;';
                                
#                             }} 
#                             event.preventDefault();
#                         }}

#                         const sidebarSectionCloseBtn = window.parent.document.body.querySelectorAll('section[class="custom-sidebar"]  div[class="close-btn-small-screen"]');
#                         sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
#                     </script> 

#                     '''
#         st.components.v1.html(js_el_, height=0, width=0) 

    
#     def openCloseButtonAutoColor(self):

#         st.html(
#             '''
#                 <style>
#                     i[id="close-sidebar-btn-icon"]{
#                         color: var(--default-textColor) !important;
#                     } 
#                 </style>
#             '''
#         )
    
#     def clicked_page(self, key="testing"):
#         """
#         Get the navigation user has just clicked
#         """

#         component_value = _sidebar_component(initialPage=self.loadPageName, key=key, default=self.loadPageName)

#         return component_value

#     def change_page(self):

#         """
#         Changes page using streamlit's native `switch_page`. If you wish to use this function, `loadPageName` is required. Cannot be None.
#         """

#         if "currentPage" not in st.session_state:
#             st.session_state["currentPage"] = self.loadPageName
#         else:
#             st.session_state["currentPage"] = self.loadPageName
        
#         if "clicked_page_" not in st.session_state:
#             st.session_state["clicked_page_"] = None

#         st.session_state["clicked_page_"] = self.clicked_page()

#         if st.session_state["clicked_page_"] != None and st.session_state["clicked_page_"] != self.loadPageName:
            
#             pages_data = self.data
#             pages_data.extend(self.base_data)
#             for i in range(len(pages_data)):
#                 pages_data[i]["index"] = i 
#             keyValList = [st.session_state["clicked_page_"]]
#             expectedResult = [d for d in pages_data if d['page_name'] in keyValList]
#             st.switch_page(expectedResult[0]["page_name_programmed"])
        
#     def load_custom_sidebar(self):
#         """
#         Salad of methods used to create final sidebar. If you wish to use this function, `loadPageName` is required. Cannot be None.
#         """

#         with st.container(height=1, border=False):
#             st.html(
#                 """
#                     <style>
#                         div[height='1']{
#                             display:none;
#                         }
#                     </style>
#                 """
#             )
          
#             emojis_load = SidebarIcons(self.iframeContainer)
#             if self.webMedium == "local":
#                 emojis_load.Load_All_CDNs()
#             elif self.webMedium == "streamlit-cloud":
#                 emojis_load.Load_All_CDNs_to_streamlit_cloud()
#             elif self.webMedium == "custom":
#                 emojis_load.custom_query_for_my_app_head_tag_CDN()

#             self.sidebarCreate() 
#             self.hover_over_siebar_navigations()
#             self.active_navigation()
#             self.close_sidebar()
#             self.close_sidebar_small_screen()
#             self.closed_btn_small_screen_first_load()
#             self.closed_btn_small_screen()
#             if self.closeBtnColor == "auto":
#                 self.openCloseButtonAutoColor() 
#             self.change_page()



current_page = "example"


data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/"},
            {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

base_data_ = [
    {"index":0, "label":"Settings", "page_name":"settings", "page_name_programmed":"None", "icon":"settings", "iconLib":"Google"},
    {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
]

footer_data = [
    {"index":0, "label":"Feedback", "page_name":"settings", "page_name_programmed":"None", "icon":"help_center", "iconLib":"Google", "href":"https://google.co.uk"},
    # {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
]

test_sidebar_ = NoHoverExpandSidebarTemplate(closedOnLoad=False, base_data=base_data_, data=data_, footer_data=footer_data, logoUrl="https://www.google.co.uk", logoText="Optum Gamer", logoTextSize="20px", headlineText="4 days left in your free trial", mainText="Get access to all data available on the platform.", informationLink="https://google.co.uk")
test_sidebar_.load_custom_sidebar()
# active_navigation()

st.write("**Sup Bro**")
# st.write("**Hey Man, Bro**")



