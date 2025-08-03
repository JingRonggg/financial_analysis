interface WidgetProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

const Widget: React.FC<WidgetProps> = ({ title, children, className = '' }) => {
  return (
    <div className={`widget ${className}`}>
      <div className="widget-header">
        <h3>{title}</h3>
      </div>
      <div className="widget-content">
        {children}
      </div>
    </div>
  );
};

export default Widget;