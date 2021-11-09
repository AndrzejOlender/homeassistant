import{_ as i,H as t,e,a as o,m as a,T as r,b as s,c as d,s as n,d as l,r as c,n as h}from"./main-60575625.js";import"./c.b82b3683.js";import"./c.5bd359ff.js";import"./c.75898fa6.js";import{f as p,h as u}from"./c.149491ec.js";import"./c.a1ea1e73.js";import"./c.6dff8de3.js";import"./c.0f3aa98b.js";import"./c.40bbc652.js";import"./c.386ba692.js";import"./c.5325c693.js";import"./c.d3dbc78b.js";let f=i([h("hacs-add-repository-dialog")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[e({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[e({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[e()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[e()],key:"_sortBy",value:()=>"stars"},{kind:"field",decorators:[e()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach((i,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),i.has("narrow")||i.has("filters")||i.has("active")||i.has("_searchInput")||i.has("_load")||i.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(i,t)=>null==i?void 0:i.filter(i=>{var e,o;return!i.installed&&(null===(e=this.hacs.sections)||void 0===e||null===(o=e.find(i=>i.id===this.section).categories)||void 0===o?void 0:o.includes(i.category))&&!i.installed&&(null==t?void 0:t.includes(i.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var i;if(this.addEventListener("filter-change",i=>this._updateFilters(i)),0===(null===(i=this.filters)||void 0===i?void 0:i.length)){var t;const i=null===(t=o(this.hacs.language,this.route))||void 0===t?void 0:t.categories;null==i||i.filter(i=>{var t;return null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories.includes(i)}).forEach(i=>{this.filters.push({id:i,value:i,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(i){const t=this.filters.find(t=>t.id===i.detail.id);this.filters.find(i=>i.id===t.id).checked=!t.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>a(p)},{kind:"method",key:"render",value:function(){var i;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("hacs-search")||"";let t=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(i=this.hacs.configuration)||void 0===i?void 0:i.categories),this._searchInput);return 0!==this.filters.length&&(t=t.filter(i=>{var t;return null===(t=this.filters.find(t=>t.id===i.category))||void 0===t?void 0:t.checked})),r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("dialog_add_repo.title")}
        hideActions
      >
        <div class="searchandfilter">
          <search-input
            no-label-float
            .label=${this.hacs.localize("search.placeholder")}
            .filter=${this._searchInput||""}
            @value-changed=${this._inputValueChanged}
            ?narrow=${this.narrow}
          ></search-input>
          <div class="filter">
            <ha-paper-dropdown-menu
              label="${this.hacs.localize("dialog_add_repo.sort_by")}"
              ?narrow=${this.narrow}
            >
              <paper-listbox slot="dropdown-content" selected="0">
                <paper-item @tap=${()=>this._sortBy="stars"}
                  >${this.hacs.localize("store.stars")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="name"}
                  >${this.hacs.localize("store.name")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="last_updated"}
                  >${this.hacs.localize("store.last_updated")}</paper-item
                >
              </paper-listbox>
            </ha-paper-dropdown-menu>
          </div>
        </div>
        ${this.filters.length>1?r`<div class="filters">
              <hacs-filter .hacs=${this.hacs} .filters="${this.filters}"></hacs-filter>
            </div>`:""}
        <div class=${s({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${s({list:!0,narrow:this.narrow})}>
            ${t.sort((i,t)=>"name"===this._sortBy?i.name.toLocaleLowerCase()<t.name.toLocaleLowerCase()?-1:1:i[this._sortBy]>t[this._sortBy]?-1:1).slice(0,this._load).map(i=>r`<paper-icon-item
                  class=${s({narrow:this.narrow})}
                  @click=${()=>this._openInformation(i)}
                >
                  ${"integration"===i.category?r`
                        <img
                          loading="lazy"
                          src="https://brands.home-assistant.io/_/${i.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body two-line
                    >${i.name}
                    <div class="category-chip">
                      <hacs-chip
                        .icon=${u}
                        .value=${this.hacs.localize("common."+i.category)}
                      ></hacs-chip>
                    </div>
                    <div secondary>${i.description}</div>
                  </paper-item-body>
                </paper-icon-item>`)}
            ${0===t.length?r`<p>${this.hacs.localize("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(i){const t=i.target.scrollTop;t>=this._top?this._load+=1:this._load-=1,this._top=t}},{kind:"method",key:"_inputValueChanged",value:function(i){this._searchInput=i.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(i){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:i.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(i){i.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(i){i.target&&(i.target.outerHTML=`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[n,l,c`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 70vh;
        }

        .filter {
          margin-top: -12px;
          display: flex;
          width: 200px;
          float: right;
        }

        .list {
          margin-top: 16px;
          width: 1024px;
          max-width: 100%;
        }
        .category-chip {
          position: absolute;
          top: 8px;
          right: 8px;
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        search-input {
          float: left;
          width: 60%;
          border-bottom: 1px var(--mdc-theme-primary) solid;
        }
        search-input[narrow],
        div.filter[narrow],
        ha-paper-dropdown-menu[narrow] {
          width: 100%;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
          position: absolute;
        }

        paper-icon-item:focus {
          background-color: var(--divider-color);
        }

        paper-icon-item {
          cursor: pointer;
          padding: 2px 0;
        }

        ha-paper-dropdown-menu {
          margin: 0 12px 4px 0;
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-icon-item.narrow {
          border-bottom: 1px solid var(--divider-color);
          padding: 8px 0;
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add {
          border-top: 1px solid var(--divider-color);
          margin-top: 32px;
        }
        .filters {
          width: 100%;
          display: flex;
        }
        .add-actions {
          justify-content: space-between;
        }
        .add,
        .add-actions {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: 65px;
          background-color: var(--sidebar-background-color);
          border-bottom: 1px solid var(--divider-color);
          padding: 0 16px;
          box-sizing: border-box;
        }
        .add-input {
          width: calc(100% - 80px);
          height: 40px;
          border: 0;
          padding: 0 16px;
          font-size: initial;
          color: var(--sidebar-text-color);
          font-family: var(--paper-font-body1_-_font-family);
        }
        input:focus {
          outline-offset: 0;
          outline: 0;
        }
        input {
          background-color: var(--sidebar-background-color);
        }

        hacs-filter {
          width: 100%;
        }
        div[secondary] {
          width: 88%;
        }
      `]}}]}}),t);export{f as HacsAddRepositoryDialog};
