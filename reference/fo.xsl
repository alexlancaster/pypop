<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

 <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/fo/docbook.xsl"/>

 <xsl:import href="citation.xsl"/>
 <xsl:import href="biblio.xsl"/> 
 <xsl:import href="pagesetup.xsl"/>

 <xsl:param name="headers.on.blank.pages" select="0"/>
 <xsl:param name="footers.on.blank.pages" select="0"/>

 <xsl:param name="page.margin.top">0.3in</xsl:param>
 <xsl:param name="page.margin.bottom">0.40in</xsl:param>
 <xsl:param name="page.margin.inner">0.60in</xsl:param>
 <xsl:param name="page.margin.outer">0.70in</xsl:param>
 <xsl:param name="body.margin.top">0.5in</xsl:param>
 <xsl:param name="body.margin.bottom">0.5in</xsl:param>

 <xsl:param name="body.font.family">Helvetica</xsl:param>
 <xsl:param name="title.font.family">Helvetica</xsl:param>
 <xsl:param name="monospace.font.family">Courier</xsl:param>
 <xsl:param name="sans.font.family">Helvetica</xsl:param>
 <xsl:param name="dingbat.font.family">Times Roman</xsl:param>

 <xsl:param name="title.margin.left" select="'0.0in'"/>
 <xsl:param name="toc.indent.width" select="8"/>


 <xsl:param name="insert.xref.page.number" select="1"/>

 <!-- page citation in format (see p.45) -->
 <xsl:param name="local.l10n.xml" select="document('')"/> 
 <l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0"> 
  <l:l10n language="en"> 
   <l:context name="xref"> 
    <l:template name="page.citation" text=" (see p.%p)"/>
   </l:context>    
  </l:l10n>
 </l:i18n>

 <xsl:template match="varname">
  <xsl:call-template name="inline.italicmonoseq"/>
 </xsl:template>

 <xsl:template match="application">
  <xsl:call-template name="inline.monoseq"/>
 </xsl:template>

 <xsl:template match="phrase[@role='strong']">
  <xsl:call-template name="inline.boldseq"/>
 </xsl:template>

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
