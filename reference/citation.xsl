<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

 <xsl:param name="use.natbib.citation.in.role" select="1"/>

 <xsl:template match="biblioentry|bibliomixed" mode="citation-to-prefix">
  <xsl:text>[</xsl:text>
 </xsl:template>
 
 <xsl:template match="biblioentry|bibliomixed" mode="citation-to-suffix">
  <xsl:text>]</xsl:text>
 </xsl:template>

 <xsl:template match="citation" name="citation">
  <xsl:variable name="targets" select="key('id',.)"/>
  <xsl:variable name="target" select="$targets[1]"/>
  <xsl:variable name="refelem" select="local-name($target)"/>

  <xsl:call-template name="check.id.unique">
    <xsl:with-param name="linkend" select="@linkend"/>
  </xsl:call-template>

  <xsl:call-template name="anchor"/>

  <xsl:choose>
    <xsl:when test="count($target) = 0">
      <xsl:message>
	<xsl:text>Citation to nonexistent id: </xsl:text>
	<xsl:value-of select="."/>
      </xsl:message>
      <xsl:text>???</xsl:text>
    </xsl:when>

    <xsl:when test="$target/@xreflabel">
      <a>
        <xsl:attribute name="href">
          <xsl:call-template name="href.target">
            <xsl:with-param name="object" select="$target"/>
          </xsl:call-template>
        </xsl:attribute>
        <xsl:call-template name="xref.xreflabel">
          <xsl:with-param name="target" select="$target"/>
        </xsl:call-template>
      </a>
    </xsl:when>

   <xsl:otherwise>
    <xsl:variable name="href">
     <xsl:call-template name="href.target">
      <xsl:with-param name="object" select="$target"/>
     </xsl:call-template>
    </xsl:variable>
    
    <xsl:apply-templates select="$target" mode="citation-to-prefix"/>
    
    <a href="{$href}">
     <xsl:if test="$target/title or $target/*/title">
      <xsl:attribute name="title">
       <xsl:apply-templates select="$target" mode="citation-title"/>
      </xsl:attribute>
     </xsl:if>
     <xsl:apply-templates select="$target" mode="citation-to">
      <xsl:with-param name="referrer" select="."/>
      <xsl:with-param name="xrefstyle" select="@role"/>
     </xsl:apply-templates>
    </a>
    
    <xsl:apply-templates select="$target" mode="citation-to-suffix"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template name="natbib-text">
  <xsl:param name="entry"/>
  <xsl:param name="citationstyle" select="'citep'"/>

  <xsl:message>citationstyle: <xsl:value-of select="$citationstyle"/></xsl:message>

  <xsl:message><xsl:value-of select="name($entry)"/>: <xsl:value-of
  select="$entry/*/author"/></xsl:message>

  <xsl:variable name="authors" select="$entry//author"/>
  <xsl:variable name="year" select="$entry/*/pubdate[1]"/>

  <xsl:variable name="authortext">
   <xsl:choose>

    <xsl:when test="count($authors) = 0">
     <xsl:message>No authors specified: need authors if natbib is used</xsl:message>
    </xsl:when>
    
    <xsl:when test="count($authors) = 1">
     <xsl:value-of select="$authors/surname"/>
    </xsl:when>
    
    <xsl:when test="count($authors) = 2">
     <xsl:value-of select="$authors[1]/surname"/>
     <xsl:text> &amp; </xsl:text>
     <xsl:value-of select="$authors[2]/surname"/>
    </xsl:when>
    
    <xsl:otherwise>
     <xsl:value-of select="$authors[1]/surname"/>
     <xsl:text> et al.</xsl:text>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:message>authortext: <xsl:value-of select="$authortext"/></xsl:message>

  <xsl:choose>
   <xsl:when test="$citationstyle='citet'">
    <xsl:value-of select="$authortext"/>
    <xsl:text> (</xsl:text>
    <xsl:value-of select="$year"/>
    <xsl:text>)</xsl:text>
   </xsl:when> 

   <xsl:when test="$citationstyle='citep'">
    <xsl:text> (</xsl:text>
    <xsl:value-of select="$authortext"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$year"/>
    <xsl:text>)</xsl:text>

   </xsl:when>

   <xsl:otherwise>
    <xsl:message>Unrecognized citationstyle: <xsl:value-of
    select="$citationstyle"/>
    </xsl:message>
   </xsl:otherwise>

  </xsl:choose>


 </xsl:template>

 <xsl:template match="biblioentry|bibliomixed" mode="citation-to">
  <xsl:param name="referrer"/>
  <xsl:param name="xrefstyle"/>

  <xsl:message>xrefstyle: <xsl:value-of select="$xrefstyle"/></xsl:message>
  
  <!-- handles both biblioentry and bibliomixed -->
  <xsl:choose>

   <xsl:when test="string(.) = ''">
    <xsl:variable name="bib" select="document($bibliography.collection)"/>
    <xsl:variable name="id" select="@id"/>
    <xsl:variable name="entry" select="$bib/bibliography/*[@id=$id][1]"/>
    <xsl:choose>
     <xsl:when test="$entry">
      
      <xsl:choose>
       <xsl:when test="$use.natbib.citation.in.role != 1">
	
	<xsl:choose>
	 <xsl:when test="local-name($entry/*[1]) = 'abbrev'">
	  <xsl:apply-templates select="$entry/*[1]"/>
	 </xsl:when>
	 <xsl:otherwise>
	  <xsl:value-of select="@id"/>
	 </xsl:otherwise>
	</xsl:choose>

       </xsl:when>
       
       <xsl:otherwise>
	<xsl:call-template name="natbib-text">
	 <xsl:with-param name="entry" select="$entry"/>
	 <xsl:with-param name="citationstyle" select="$xrefstyle"/>
	</xsl:call-template>
       </xsl:otherwise>

      </xsl:choose>

     </xsl:when>
     
     <xsl:otherwise>
      <xsl:message>
       <xsl:text>No bibliography entry: </xsl:text>
       <xsl:value-of select="$id"/>
       <xsl:text> found in </xsl:text>
       <xsl:value-of select="$bibliography.collection"/>
      </xsl:message>
      <xsl:value-of select="@id"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:when>
   
   <xsl:otherwise>

    <xsl:choose>
     <xsl:when test="$use.natbib.citation.in.role != 1">
      
      <xsl:choose>
       <xsl:when test="local-name(*[1]) = 'abbrev'">
	<xsl:apply-templates select="*[1]"/>
       </xsl:when>
       <xsl:otherwise>
	<xsl:value-of select="@id"/>
       </xsl:otherwise>
      </xsl:choose>
      
     </xsl:when>

     <xsl:otherwise>
      <xsl:call-template name="natbib-text">
       <xsl:with-param name="entry" select="."/>
       <xsl:with-param name="citationstyle" select="$xrefstyle"/>
      </xsl:call-template>

     </xsl:otherwise>

    </xsl:choose>
    
   </xsl:otherwise>

  </xsl:choose>
 </xsl:template>
 
<xsl:template match="biblioentry|bibliomixed" mode="citation-title">
  <!-- handles both biblioentry and bibliomixed -->
  <xsl:variable name="title">
    <xsl:text>[</xsl:text>
    <xsl:choose>
      <xsl:when test="local-name(*[1]) = 'abbrev'">
        <xsl:apply-templates select="*[1]"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="@id"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>]</xsl:text>
  </xsl:variable>

  <xsl:value-of select="$title"/>
</xsl:template>


</xsl:stylesheet>

