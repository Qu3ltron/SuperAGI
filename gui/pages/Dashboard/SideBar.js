import React, {useState} from 'react';
import Image from 'next/image';
import styles from './Dashboard.module.css';
import {refreshUrl, openNewTab} from "@/utils/utils";

export default function SideBar({onSelectEvent}) {
  const [sectionSelected, setSelection] = useState('');

  const handleClick = (value) => {
    setSelection(value);
    onSelectEvent(value);
    if (value === 'apm') {
      openNewTab(-9, "APM", "APM");
    }
  };

  return (
    <div className={styles.side_bar}>
      <div><Image width={64} height={48} className={styles.logo} src="/images/app-logo-light.png" alt="super-agi-logo"/>
      </div>
      <div className={styles.selection_section}>
        <div onClick={() => handleClick(sectionSelected !== 'agents' ? 'agents' : '')}
             className={`${styles.section} ${sectionSelected === 'agents' ? styles.selected : ''}`}>
          <div className={styles.button_icon}><Image width={17} height={17} src="/images/agents_light.svg"
                                                     alt="agent-icon"/></div>
          <div>Agents</div>
        </div>
      </div>
      <div className={styles.selection_section}>
        <div onClick={() => handleClick(sectionSelected !== 'toolkits' ? 'toolkits' : '')}
             className={`${styles.section} ${sectionSelected === 'toolkits' ? styles.selected : ''}`}>
          <div className={styles.button_icon}><Image width={17} height={17} src="/images/tools_light.svg"
                                                     alt="tools-icon"/></div>
          <div>Toolkits</div>
        </div>
      </div>
      <div className={styles.selection_section}>
        <div onClick={() => handleClick(sectionSelected !== 'apm' ? 'apm' : '')}
             className={`${styles.section} ${sectionSelected === 'apm' ? styles.selected : ''}`}>
          <div className={styles.button_icon}><Image width={17} height={17} src="/images/apm.svg" alt="apm-icon"/></div>
          <div>APM</div>
        </div>
      </div>
    </div>
  );
}
